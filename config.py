import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    class Config:
        env_file = ".env"

    APP_PORT: int
    APP_HOST: str
    APP_DEBUG: bool

    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SECRET_KEY: str


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

app_run = {
    "host": app_conf.APP_HOST,
    "port": app_conf.APP_PORT,
    "debug": app_conf.APP_DEBUG
}
