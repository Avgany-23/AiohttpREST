import pydantic_settings


class UserDataParamsConfig(pydantic_settings.BaseSettings):
    min_passw_length: int = 8
    max_passw_length: int = 100

    min_name_length: int = 5
    max_name_length: int = 50


user_data = UserDataParamsConfig()
