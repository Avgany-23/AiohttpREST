from flask import json


def test_check_found_user_data(api_client, session):
    headers = {"content-type": "application/json"}
    username = "name_one"
    data = json.dumps({"username": username, "password": "12345Qq!"})
    api_client.post('api/v1/user/registration', headers=headers, data=data)
    response = api_client.get(f'api/v1/user/check/{username}', headers=headers, data=data)
    assert response.status_code == 200


def test_check_not_found_user_data(api_client, session):
    headers = {"content-type": "application/json"}
    response = api_client.get('api/v1/user/check/name_one', headers=headers)
    assert response.status_code == 404
