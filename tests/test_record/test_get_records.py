from apps.record.config import record_conf
from apps.record import ModelRecord
from apps.user import ModelUser
import json
import pytest


async def test_get_all_records(api_client, header_user):
    for i in range(record_conf.LIMIT_CREATED_RECORD_FOR_USER + 1):
        await api_client.post('api/v1/record', headers=header_user, data=json.dumps({"title": str(i)}))
    response = await api_client.get('api/v1/record', headers=header_user)
    assert response.status == 200
    assert len((await response.json())['records']) == 10


@pytest.mark.parametrize("count", [1, 5, 7, 10])
async def test_get_correct_count_records(api_client, header_user, sync_session, count):
    id_user = sync_session.query(ModelUser).first().id
    sync_session.add_all([ModelRecord(title=i, owner=id_user) for i in range(12)])
    sync_session.commit()
    response = await api_client.get('api/v1/record?%s' % f"count={count}", headers=header_user)
    assert len((await response.json())['records']) == count


@pytest.mark.parametrize("count", [11, 15, 20])
async def test_get_incorrect_count_records(api_client, header_user, sync_session, count):
    id_user = sync_session.query(ModelUser).first().id
    sync_session.add_all([ModelRecord(title=i, owner=id_user) for i in range(17)])
    sync_session.commit()
    response = await api_client.get('api/v1/record?%s' % f"count={count}", headers=header_user)
    assert response.status == 400
