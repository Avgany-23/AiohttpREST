import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    class Config:
        env_file = ".env"

    APP_PORT: int = 8000
    APP_HOST: str = 'localhost'
    APP_DEBUG: bool = True

    POSTGRES_NAME: str = 'postgresql'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = '1234'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'postgres'

    SECRET_KEY: str = '...'


class PsqlConfig(pydantic_settings.BaseSettings):
    _psql: Settings = Settings()

    POSTGRES_NAME: str = _psql.POSTGRES_NAME
    POSTGRES_USER: str = _psql.POSTGRES_USER
    POSTGRES_PASSWORD: int = _psql.POSTGRES_PASSWORD
    POSTGRES_HOST: str | int = _psql.POSTGRES_HOST
    POSTGRES_PORT: int = _psql.POSTGRES_PORT
    POSTGRES_DB: str = _psql.POSTGRES_DB


class AppConfig(pydantic_settings.BaseSettings):
    _app: Settings = Settings()  # noqa

    APP_PORT: int = _app.APP_PORT
    APP_HOST: str = _app.APP_HOST
    APP_DEBUG: bool = _app.APP_DEBUG


psql_settings: PsqlConfig = PsqlConfig()

app_conf = AppConfig()

psql_url: str = (
    f"{psql_settings.POSTGRES_NAME}://"
    f"{psql_settings.POSTGRES_USER}:{psql_settings.POSTGRES_PASSWORD}@"
    f"{psql_settings.POSTGRES_HOST}:{psql_settings.POSTGRES_PORT}/"
    f"{psql_settings.POSTGRES_DB}"
)

async_psql_url: str = (
    f"{psql_settings.POSTGRES_NAME}+asyncpg://"
    f"{psql_settings.POSTGRES_USER}:{psql_settings.POSTGRES_PASSWORD}@"
    f"{psql_settings.POSTGRES_HOST}:{psql_settings.POSTGRES_PORT}/"
    f"{psql_settings.POSTGRES_DB}"
)

app_run = {
    "host": app_conf.APP_HOST,
    "port": app_conf.APP_PORT,
}
