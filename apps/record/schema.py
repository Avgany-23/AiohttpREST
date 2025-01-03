from pydantic import BaseModel, constr, conint, field_validator
import datetime


class BaseTitle:
    title: constr(min_length=1, max_length=50)


class RecordSchema(BaseModel, BaseTitle):
    id: int
    description: str | None = None
    date_created: datetime.datetime
    owner: int

    @field_validator('date_created', mode='after')
    def format_date(cls, value: datetime) -> str:
        return value.strftime('%Y-%m-%d %H:%M:%S')


class RecordQueryGetSerializer(BaseModel):
    title: constr(min_length=1, max_length=50) = None
    count: conint(gt=0, le=10) = None


class RecordBodyCreateSerializer(BaseModel, BaseTitle):
    description: str = None


class RecordBodyUpdateSerializer(BaseModel):
    title: constr(min_length=1, max_length=50) = None
    description: str = None
