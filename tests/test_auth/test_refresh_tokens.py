from apps.auth.exceptions import ErrorExpiredToken
import json


async def test_update_tokens_with_correct_refresh(api_client, create_tokens):
    old_refresh = create_tokens.get("refresh")
    data = json.dumps({"token": old_refresh})
    response = await api_client.post('/api/v1/auth/refresh', data=data)
    data = await response.json()
    refresh = data.get("refresh")
    access = data.get("access")
    assert response.status == 201
    assert "access" in data and "refresh" in data
    assert refresh != old_refresh and access != old_refresh


async def test_update_tokens_with_invalid_refresh(api_client, create_tokens):
    data = json.dumps({"token": create_tokens.get("refresh") + "0"})
    response = await api_client.post('api/v1/auth/refresh', data=data)
    assert response.status == 400
    assert await response.json() == {'token error': 'Invalid token'}


async def test_update_tokens_with_expired_refresh(mocker, api_client, create_tokens):
    mock_get_external_data = mocker.patch('apps.auth.service.refresh_token')
    mock_get_external_data.side_effect = ErrorExpiredToken

    data = json.dumps({"token": create_tokens.get("refresh")})
    response = await api_client.post('api/v1/auth/refresh', data=data)
    assert response.status == 400
    assert await response.json() == {'token error': 'Expired time life token'}
