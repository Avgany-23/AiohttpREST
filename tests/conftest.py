from db import basic, AsyncDatabaseHelper, DatabaseHelper
from config import async_psql_url
import sqlalchemy as sql
import pytest_asyncio
from aiohttp import web
from apps import routers
import middleware
import pytest
import json


pytest_plugins = 'aiohttp.pytest_plugin'


"""Обязательный импорт, чтобы metadata заполнилась данными с таблиц"""
import apps.record.models  # noqa
import apps.user.models  # noqa


@pytest.fixture(scope='function')
async def api_client(aiohttp_client):
    app = web.Application(
        middlewares=middleware.apps_middleware + [
            middleware.middleware_pydantic_validation,
            middleware.middleware_auth,
            middleware.middleware_json_error_encoder,
        ]
    )
    for rout in routers:
        app.add_routes(rout)
    return await aiohttp_client(app)


@pytest_asyncio.fixture(scope='function')
async def session():
    db = AsyncDatabaseHelper()
    async with db.session_factory() as session:
        yield session
        await session.close()


@pytest.fixture(scope='function')
def sync_session():
    session = DatabaseHelper().get_session()
    yield session
    session.close()


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clear_db(session):
    yield
    for table in reversed(basic.metadata.sorted_tables):
        await session.execute(sql.text(f"TRUNCATE TABLE \"{table}\" RESTART IDENTITY CASCADE;"))
    await session.commit()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db():
    key_db_test = 'test'
    assert key_db_test in async_psql_url, 'В тестовом подключении к БД должно быть слово %s' % key_db_test

    db = AsyncDatabaseHelper()
    engine = db.engine
    async with engine.begin() as conn:
        await conn.run_sync(basic.metadata.drop_all)
        await conn.run_sync(basic.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(basic.metadata.drop_all)


@pytest.fixture
def user_data():
    return {"username": "name_one", "password": "12345Qq!"}


@pytest.fixture(scope='function')
async def create_user(api_client, user_data):
    data = json.dumps({**user_data})
    await api_client.post('api/v1/user/registration', data=data)
    return user_data


@pytest.fixture(scope='function')
async def create_tokens(api_client, create_user):
    data = json.dumps({**create_user})
    response = await api_client.post('api/v1/auth/login', data=data)
    return await response.json()


@pytest.fixture(scope='function')
async def create_access(api_client, create_user):
    data = json.dumps({**create_user})
    response = await api_client.post('api/v1/auth/login', data=data)
    return (await response.json()).get("access")


@pytest.fixture(scope='function')
async def header_user(create_access):
    return {"content-type": "application/json", "Authorization": "Bearer " + create_access}
