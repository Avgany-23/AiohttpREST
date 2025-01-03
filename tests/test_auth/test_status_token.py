from apps.auth.exceptions import ErrorExpiredToken
import json
import pytest


@pytest.mark.parametrize("type_token", ["refresh", "access"])
async def test_status_tokens_with_correct_tokens(api_client, create_tokens, type_token):
    data = json.dumps({"token": create_tokens.get(type_token)})
    response = await api_client.get('api/v1/auth/status', data=data)
    assert response.status == 200
    assert await response.json() == {'token': 'Active'}


@pytest.mark.parametrize("type_token", ["refresh", "access"])
async def test_status_tokens_with_invalid_tokens(api_client, create_tokens, type_token):
    data = json.dumps({"token": create_tokens.get(type_token) + '0'})
    response = await api_client.get('api/v1/auth/status', data=data)
    assert response.status == 400
    assert await response.json() == {'token error': 'Invalid token'}


@pytest.mark.parametrize("type_token", ["refresh", "access"])
async def test_status_tokens_with_expired_tokens(mocker, api_client, create_tokens, type_token):
    mock_get_external_data = mocker.patch('apps.auth.service.status_jwt_for_user')
    mock_get_external_data.side_effect = ErrorExpiredToken

    data = json.dumps({"token": create_tokens.get(type_token) + '0'})
    response = await api_client.get('api/v1/auth/status', data=data)
    assert response.status == 400
    assert await response.json() == {'token error': 'Expired time life token'}
