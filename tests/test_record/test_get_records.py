from apps.record.config import record_conf
from apps.record import ModelRecord
from apps.user import ModelUser
from flask import json
import pytest


def test_get_all_records(api_client, header_user, session):
    for i in range(record_conf.LIMIT_CREATED_RECORD_FOR_USER + 1):
        api_client.post('api/v1/record', headers=header_user, data=json.dumps({"title": str(i)}))
    response = api_client.get('api/v1/record', headers=header_user)
    assert response.status_code == 200
    assert len(response.json['records']) == 10


@pytest.mark.parametrize("count", [1, 5, 7, 10])
def test_get_correct_count_records(api_client, header_user, session, count):
    id_user = session.query(ModelUser).first().id
    session.add_all([ModelRecord(title=i, owner=id_user) for i in range(12)])
    session.commit()
    response = api_client.get('api/v1/record?%s' % f"count={count}", headers=header_user)
    assert len(response.json['records']) == count


@pytest.mark.parametrize("count", [11, 15, 20])
def test_get_incorrect_count_records(api_client, header_user, session, count):
    id_user = session.query(ModelUser).first().id
    session.add_all([ModelRecord(title=i, owner=id_user) for i in range(17)])
    session.commit()
    response = api_client.get('api/v1/record?%s' % f"count={count}", headers=header_user)
    assert response.status_code == 400
