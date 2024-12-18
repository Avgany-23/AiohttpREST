import pydantic_settings


class RecordsConfig(pydantic_settings.BaseSettings):
    LIMIT_CREATED_RECORD_FOR_USER: int = 10


record_conf = RecordsConfig()
