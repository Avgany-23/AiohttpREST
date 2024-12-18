from apps.auth.exception import ErrorExpiredToken
from flask import json


def test_update_tokens_with_correct_refresh(api_client, create_tokens):
    headers = {"content-type": "application/json"}
    old_refresh = create_tokens.get("refresh")
    data = json.dumps({"token": old_refresh})
    response = api_client.post('/api/v1/auth/refresh', headers=headers, data=data)
    refresh = response.json.get("refresh")
    access = response.json.get("access")
    assert response.status_code == 201
    assert "access" in response.json and "refresh" in response.json
    assert refresh != old_refresh and access != old_refresh


def test_update_tokens_with_invalid_refresh(api_client, create_tokens):
    headers = {"content-type": "application/json"}
    data = json.dumps({"token": create_tokens.get("refresh") + "0"})
    response = api_client.post('api/v1/auth/refresh', headers=headers, data=data)
    assert response.status_code == 400
    assert response.json == {'status token': 'Invalid token'}


def test_update_tokens_with_expired_refresh(mocker, api_client, create_tokens):
    mock_get_external_data = mocker.patch('apps.auth.main.refresh_token')
    mock_get_external_data.side_effect = ErrorExpiredToken

    headers = {"content-type": "application/json"}
    data = json.dumps({"token": create_tokens.get("refresh")})
    response = api_client.post('api/v1/auth/refresh', headers=headers, data=data)
    assert response.status_code == 400
    assert response.json == {'status token': 'Expired time life token'}
