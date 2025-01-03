import pytest
import json


@pytest.mark.parametrize("data,status_code", [
    ({"username": "name_one", "password": "12345Qq!"}, 201),
    ({"username": "name_", "password": "12345Qq!"}, 201),
    ({"username": "user", "password": "12345Qq!"}, 400),
    ({"username": "name_one", "password": "1112345Qq"}, 400),
    ({"username": "name_one", "password": "1112345Q!"}, 400),
    ({"username": "name_one", "password": "1112345q!"}, 400),
    ({"username": "name_one", "password": "1115Qq!"}, 400),
    ({"username": "n" * 51, "password": "Qq!" * 33}, 400),
    ({"username": "n" * 50, "password": "Qq!" * 34}, 400),
])
async def test_registration(api_client, data, status_code):
    headers = {"content-type": "application/json"}
    data = json.dumps({**data})
    response = await api_client.post('api/v1/user/registration', headers=headers, data=data)
    assert response.status == status_code


async def test_duplicate_username(api_client):
    headers = {"content-type": "application/json"}
    user1 = {"username": "name_one", "password": "12345Qq!"}
    user2 = {"username": "name_one", "password": "FJ394fk5Qq!"}
    data1 = json.dumps({**user1})
    data2 = json.dumps({**user2})
    await api_client.post('api/v1/user/registration', headers=headers, data=data1)
    response = await api_client.post('api/v1/user/registration', headers=headers, data=data2)
    assert response.status == 400
