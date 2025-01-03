import json


async def test_get_access_with_exist_user(api_client, create_user):
    data = json.dumps({**create_user})
    response = await api_client.post('api/v1/auth/login', data=data)
    data = (await response.json())
    assert response.status == 201
    assert "access" in data and "refresh" in data


async def test_get_access_with_not_exist_user(api_client, user_data):
    data = json.dumps({**user_data})
    response = await api_client.post('api/v1/auth/login', data=data)
    data = (await response.json())
    assert response.status == 400
    assert "access" not in data and "refresh" not in data


async def test_get_access_with_exist_user_and_incorrect_password(api_client, create_user):
    create_user['password'] = "1111111Qq!"
    data = json.dumps({**create_user})
    response = await api_client.post('api/v1/auth/login', data=data)
    data = (await response.json())
    assert response.status == 400
    assert "access" not in data and "refresh" not in data
