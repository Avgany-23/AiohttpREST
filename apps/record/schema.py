from pydantic import BaseModel, constr, conint
import datetime


class BaseTitle:
    title: constr(min_length=1, max_length=50)


class RecordSchema(BaseModel, BaseTitle):
    id: int
    description: str | None = None
    date_created: datetime.datetime
    owner: int


class RecordQueryGetSerializer(BaseModel):
    title: constr(min_length=1, max_length=50) = None
    count: conint(gt=0, le=10) = None


class RecordQueryCreateSerializer(BaseModel, BaseTitle):
    description: str = None


class RecordQueryDeleteUpdateSerializer(BaseModel, BaseTitle):
    ...


class RecordBodyDeleteUpdateSerializer(BaseModel):
    title: constr(min_length=1, max_length=50) = None
    description: str = None
    date_created: datetime.datetime = None
    owner: int = None
