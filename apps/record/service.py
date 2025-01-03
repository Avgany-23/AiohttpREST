from .exception import DuplicateRecordForUser, LimitRecordsForUser, NotFoundRecord
from sqlalchemy.exc import IntegrityError
from .config import record_conf
from utils import ForbiddenError
from .schema import RecordSchema
from utils import BaseRequest
from .models import Record
import sqlalchemy


class RecordCRUD(BaseRequest):
    table = Record


record = RecordCRUD()


async def records_count_filter(limit: int = None) -> list[dict]:
    records = [RecordSchema(**i).model_dump(warnings='none') for i in await record.get_all(limit=limit)]
    return records


async def record_title_filter(title: str) -> dict:
    result = await record.get_one(title=title)
    if result is None:
        return dict()
    return RecordSchema(**result).model_dump(warnings='none')


async def user_records(user_id: int) -> list[dict]:
    records = await record.get_several(owner=user_id)  # noqa
    response_dict = [RecordSchema(**r).model_dump(warnings='none') for r in records]
    return response_dict


class CreatedRecord:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    async def create_record(self, **kwargs) -> None:
        await self.check_quantity()
        try:
            await record.create_one(**kwargs, owner=self.user_id)
        except sqlalchemy.exc.IntegrityError:
            raise DuplicateRecordForUser

    async def check_quantity(self):
        count_records = await record.get_several(owner=self.user_id)
        if len(count_records) >= record_conf.LIMIT_CREATED_RECORD_FOR_USER:
            raise LimitRecordsForUser


class DeleteUpdateRecord:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    async def find_record(self, id_record) -> int:
        res_record = await record.get_one(id=id_record)
        if not res_record:
            raise NotFoundRecord
        if res_record.get('owner') != self.user_id:
            raise ForbiddenError
        return res_record.id

    async def delete_record(self, id_record: str | int) -> None:
        await self.find_record(id_record)
        await record.delete_record(id=id_record)

    async def update_record(self, id_record: str | int, **data) -> dict | None:
        await self.find_record(id_record)
        try:
            await record.update_record(data, id=id_record)
        except IntegrityError:
            raise DuplicateRecordForUser(msg='У вас уже есть другая статья с таким же названием')
        return RecordSchema(** await record.get_one(id=id_record)).model_dump(warnings='none')
