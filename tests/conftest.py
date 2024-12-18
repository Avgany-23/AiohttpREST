import sqlalchemy as sql
from flask import json
from app import app
import pytest
import db


engine = db.DatabaseHelper().engine


@pytest.fixture
def api_client():
    return app.test_client()


@pytest.fixture(scope='function')
def session():
    session = db.DatabaseHelper().get_session()
    yield session
    session.close()


@pytest.fixture(scope='function', autouse=True)
def clear_db(session):
    yield
    for table in reversed(db.basic.metadata.sorted_tables):
        session.execute(sql.text(f"TRUNCATE TABLE \"{table}\" RESTART IDENTITY CASCADE;"))
    session.commit()


from apps.record import ModelRecord  # noqa
from apps.user import ModelUser  # noqa


@pytest.fixture(scope="session", autouse=True)
def create_session():
    db.basic.metadata.drop_all(engine)
    db.basic.metadata.create_all(engine)
    yield
    db.basic.metadata.drop_all(engine)


@pytest.fixture
def user_data():
    return {"username": "name_one", "password": "12345Qq!"}


@pytest.fixture(scope='function')
def create_user(api_client, user_data):
    headers = {"content-type": "application/json"}
    data = json.dumps({**user_data})
    api_client.post('api/v1/user/registration', headers=headers, data=data)
    return user_data


@pytest.fixture(scope='function')
def create_tokens(api_client, create_user):
    headers = {"content-type": "application/json"}
    data = json.dumps({**create_user})
    response = api_client.post('api/v1/auth/login', headers=headers, data=data)
    return response.json


@pytest.fixture(scope='function')
def create_access(api_client, create_user):
    headers = {"content-type": "application/json"}
    data = json.dumps({**create_user})
    response = api_client.post('api/v1/auth/login', headers=headers, data=data)
    return response.json.get("access")


@pytest.fixture(scope='function')
def header_user(create_access):
    return {"content-type": "application/json", "Authorization": "Bearer " + create_access}
