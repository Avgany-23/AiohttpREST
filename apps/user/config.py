from pydantic_settings import BaseSettings


class UserDataParamsConfig(BaseSettings):
    min_passw_length: int = 8
    max_passw_length: int = 100

    min_name_length: int = 5
    max_name_length: int = 50


user_data = UserDataParamsConfig()
