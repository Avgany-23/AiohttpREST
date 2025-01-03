from apps.record.config import record_conf
from apps.record import ModelRecord
from sqlalchemy import select
import pytest
import json


@pytest.mark.parametrize("data", [
    {"title": "title", "description": "desc 1"},
    {"title": "title  1"},
    {"title": "111111111111", "description": "desc 1" * 5},
])
async def test_create_records_with_auth_user_and_correct_data(api_client, header_user, data, sync_session):
    response = await api_client.post('api/v1/record', headers=header_user, data=json.dumps(data))
    assert response.status == 201
    assert await response.json() == {'created': 'success'}
    assert sync_session.execute(select(ModelRecord)).scalar() is not None


@pytest.mark.parametrize("data", [
    {"title": "", "description": "desc 1"},
    {"title1": "title  1", "description": None},
    {"title2": "title  1", "description": "desc 1" * 5},
    {"title": "title  1" * 2000, "description": "desc 1" * 5},
])
async def test_create_records_with_auth_user_and_incorrect_data(api_client, header_user, data):
    response = await api_client.post('api/v1/record', headers=header_user, data=json.dumps(data))
    assert response.status == 400


async def test_create_records_with_non_auth_user(api_client):
    data = json.dumps({"title": "title", "description": "desc 1"})
    response = await api_client.post('api/v1/record', data=data)
    assert response.status == 401
    assert await response.json() == {'Not authentication': 'Token JWT not found'}


async def test_create_records_with_limited(api_client, header_user):
    for i in range(record_conf.LIMIT_CREATED_RECORD_FOR_USER + 2):
        response = await api_client.post('api/v1/record', headers=header_user, data=json.dumps({"title": str(i)}))
        if i + 1 == record_conf.LIMIT_CREATED_RECORD_FOR_USER + 2:
            assert response.status == 403
