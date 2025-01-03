import json


async def test_check_found_user_data(api_client):
    username = "name_one"
    data = json.dumps({"username": username, "password": "12345Qq!"})
    await api_client.post('api/v1/user/registration', data=data)
    response = await api_client.get(f'api/v1/user/check/{username}', data=data)
    assert response.status == 200


async def test_check_not_found_user_data(api_client):
    response = await api_client.get('api/v1/user/check/name_one')
    assert response.status == 404
