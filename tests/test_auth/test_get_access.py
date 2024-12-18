from flask import json


def test_get_access_with_exist_user(api_client, create_user):
    headers = {"content-type": "application/json"}
    data = json.dumps({**create_user})
    response = api_client.post('api/v1/auth/login', headers=headers, data=data)
    assert response.status_code == 201
    assert "access" in response.json and "refresh" in response.json


def test_get_access_with_not_exist_user(api_client, user_data):
    headers = {"content-type": "application/json"}
    data = json.dumps({**user_data})
    response = api_client.post('api/v1/auth/login', headers=headers, data=data)
    assert response.status_code == 400
    assert "access" not in response.json and "refresh" not in response.json


def test_get_access_with_exist_user_and_incorrect_password(api_client, create_user):
    headers = {"content-type": "application/json"}
    create_user['password'] = "1111111Qq!"
    data = json.dumps({**create_user})
    response = api_client.post('api/v1/auth/login', headers=headers, data=data)
    assert response.status_code == 400
    assert "access" not in response.json and "refresh" not in response.json
