from .exception import DuplicateRecordForUser, LimitRecordsForUser
from .config import record_conf
from utils import ForbiddenError
from .schema import RecordSchema
from utils import BaseRequest
from .models import Record
import sqlalchemy


class RecordCRUD(BaseRequest):
    table = Record


record = RecordCRUD()


def records_non_filter(limit: int = None) -> list[dict]:
    records = [RecordSchema(**i).model_dump() for i in record.get_all(limit=limit)]
    return records


def record_title_filter(title: str) -> dict:
    result = record.get_one(title=title)
    if result is None:
        return dict()
    return RecordSchema(**record.get_one(title=title)).model_dump()


def user_records(user_id: int) -> list[dict]:
    records = record.get_several(owner=user_id)  # noqa
    response_dict = [RecordSchema(**r).model_dump() for r in records]
    return response_dict


class CreatedRecord:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def create_record(self, **kwargs) -> None:
        self.check_quantity()
        try:
            record.create_one(**kwargs, owner=self.user_id)
        except sqlalchemy.exc.IntegrityError:
            raise DuplicateRecordForUser

    def check_quantity(self):
        count_records = record.get_several(owner=self.user_id)
        if len(count_records) > record_conf.LIMIT_CREATED_RECORD_FOR_USER:
            raise LimitRecordsForUser


class DeleteUpdateRecord:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def find_record(self, title: str) -> int:
        records = record.get_several(title=title)
        if not records:
            return False
        for r in records:
            if r.owner == self.user_id:
                return r.id
        raise ForbiddenError

    def delete_record(self, title: str) -> bool:
        record_id = self.find_record(title)
        if record_id:
            record.delete_record(id=record_id)
            return True
        return False

    def update_record(self, title_name: str, **data) -> dict | None:
        record_id = self.find_record(title_name)
        if record_id:
            record.update_record(data, id=record_id)
            return RecordSchema(**record.get_one(id=record_id)).model_dump()
