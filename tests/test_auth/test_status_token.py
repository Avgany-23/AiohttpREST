from apps.auth.exception import ErrorExpiredToken
from flask import json
import pytest


@pytest.mark.parametrize("type_token", ["refresh", "access"])
def test_status_tokens_with_correct_tokens(api_client, create_tokens, type_token):
    headers = {"content-type": "application/json"}
    data = json.dumps({"token": create_tokens.get(type_token)})
    response = api_client.get('api/v1/auth/status', headers=headers, data=data)
    assert response.status_code == 200
    assert response.json == {'token': 'Active'}


@pytest.mark.parametrize("type_token", ["refresh", "access"])
def test_status_tokens_with_invalid_tokens(api_client, create_tokens, type_token):
    headers = {"content-type": "application/json"}
    data = json.dumps({"token": create_tokens.get(type_token) + '0'})
    response = api_client.get('api/v1/auth/status', headers=headers, data=data)
    assert response.status_code == 400
    assert response.json == {'status token': 'Invalid token'}


@pytest.mark.parametrize("type_token", ["refresh", "access"])
def test_status_tokens_with_expired_tokens(mocker, api_client, create_tokens, type_token):
    mock_get_external_data = mocker.patch('apps.auth.main.status_jwt_for_user')
    mock_get_external_data.side_effect = ErrorExpiredToken

    headers = {"content-type": "application/json"}
    data = json.dumps({"token": create_tokens.get(type_token) + '0'})
    response = api_client.get('api/v1/auth/status', headers=headers, data=data)
    assert response.status_code == 400
    assert response.json == {'status token': 'Expired time life token'}
