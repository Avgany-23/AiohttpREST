from apps.user.config import user_data as ud
from pydantic import BaseModel, constr


class AccessSerializer(BaseModel):
    username: constr(
        min_length=ud.min_name_length,
        max_length=ud.max_name_length
    )
    password: constr(
        min_length=ud.min_passw_length,
        max_length=ud.max_passw_length
    )


class TokenSerializer(BaseModel):
    token: str
