from pydantic import BaseModel, constr, field_validator, validate_email
from pydantic_async_validation import async_field_validator, AsyncValidationModelMixin
from .config import user_data as ud
from utils import ReturnSerializer
import apps.user.exception as exc
from .service import check_user
from typing import Any
import re


class RegistrationSerializer(AsyncValidationModelMixin, BaseModel):
    username: constr(min_length=ud.min_name_length, max_length=ud.max_name_length)
    email: str | None = None
    password: str

    @async_field_validator('username')  # noqa
    async def validate_username(self, value: Any) -> None:
        if await check_user(value):
            raise exc.duplicate_username(value)

    @field_validator('email')  # noqa
    @classmethod
    def email_validate(cls, v: Any) -> ReturnSerializer:
        try:
            validate_email(v)
        except Exception as e:
            print(e)
            raise exc.incorrect_email(v) from e
        return v

    @field_validator('password')  # noqa
    @classmethod
    def password_validate(cls, v: Any) -> ReturnSerializer:
        min_, max_ = ud.min_passw_length, ud.max_passw_length
        pattern = f'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{{{min_},{max_}}}$'
        if not re.findall(pattern, v):
            raise exc.incorrect_password
        return v
