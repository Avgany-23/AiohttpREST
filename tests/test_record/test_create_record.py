from apps.record.config import record_conf
from flask import json
import pytest


@pytest.mark.parametrize("data", [
    {"title": "title", "description": "desc 1"},
    {"title": "title  1"},
    {"title": "111111111111", "description": "desc 1" * 5},
])
def test_create_records_with_auth_user_and_correct_data(api_client, header_user, data):
    response = api_client.post('api/v1/record', headers=header_user, data=json.dumps(data))
    assert response.status_code == 201
    data.setdefault("description", None)
    assert response.json == {'created': data}


@pytest.mark.parametrize("data", [
    {"title": "", "description": "desc 1"},
    {"title1": "title  1", "description": None},
    {"title2": "title  1", "description": "desc 1" * 5},
    {"title": "title  1" * 2000, "description": "desc 1" * 5},
])
def test_create_records_with_auth_user_and_incorrect_data(api_client, header_user, data):
    response = api_client.post('api/v1/record', headers=header_user, data=json.dumps(data))
    assert response.status_code == 400


def test_create_records_with_non_auth_user(api_client):
    headers = {"content-type": "application/json"}
    data = json.dumps({"title": "title", "description": "desc 1"})
    response = api_client.post('api/v1/record', headers=headers, data=data)
    assert response.status_code == 401
    assert response.json == {'error token': 'Token JWT not found'}


def test_create_records_with_limited(api_client, header_user):
    for i in range(record_conf.LIMIT_CREATED_RECORD_FOR_USER + 2):
        response = api_client.post('api/v1/record', headers=header_user, data=json.dumps({"title": str(i)}))
        if i + 1 == record_conf.LIMIT_CREATED_RECORD_FOR_USER + 2:
            assert response.status_code == 403
