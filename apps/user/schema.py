from pydantic import BaseModel, constr, field_validator, validate_email
from .config import user_data as ud
from utils import ReturnSerializer
import apps.user.exception as exc
from .service import check_user
from typing import Any
import re


class RegistrationSerializer(BaseModel):
    username: constr(min_length=ud.min_name_length, max_length=ud.max_name_length)
    email: str | None = None
    password: str

    @field_validator('username')  # noqa
    @classmethod
    def username_validate(cls, v: Any) -> ReturnSerializer:
        if check_user(v):
            raise exc.duplicate_username(v)
        return v

    @field_validator('email')  # noqa
    @classmethod
    def email_validate(cls, v: Any) -> ReturnSerializer:
        try:
            validate_email(v)
        except Exception as e:
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
