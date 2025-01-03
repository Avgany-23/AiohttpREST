from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import sqlalchemy.orm as orm
import sqlalchemy
import functools
import config
import typing


basic = orm.declarative_base()


class AsyncDatabaseHelper:
    """Класс для подключения к реляционной базе данных"""

    def __init__(
            self, url: str = config.async_psql_url,
            echo: bool = False,
            autofl: bool = True,
            expire_on_commit: bool = True
    ):

        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=autofl,
            expire_on_commit=expire_on_commit
        )


def connect_psql(
        auto_commit: bool = False,
        config_: str = config.async_psql_url,
):
    """
    Декоратор для автоматического подключения к сессии и выхода из сессии Базы Данных.
    Все ошибки, связанные с запросами SQL, декоратор записывает в логи стандартного вывода stdout.

        - при использовании декоратора в функциях либо классах,
        аргумент session должен стоять после всех позиционных аргументов.

    :param auto_commit: По умолчанию False. Для авто-коммита установить True
    :param config_: URL для подключения к БД. По умолчанию используется URL из модуля config
    Если false, то функция вернет своё значение. По умолчанию параметр False
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> typing.Any:
            database_helper = AsyncDatabaseHelper(config_)
            async with database_helper.session_factory() as session:
                try:
                    result = await func(*args, session=session, **kwargs)
                    if auto_commit:
                        await session.commit()
                    return result
                except Exception as e:
                    await session.rollback()
                    raise e
                finally:
                    await session.close()

        return wrapper

    return decorator


class DatabaseHelper:
    """Класс для подключения к реляционной базе данных"""

    def __init__(
            self, url: str = config.psql_url,
            echo: bool = False,
            autofl: bool = True,
            expire_on_commit: bool = True
    ):

        self.engine = sqlalchemy.create_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = orm.sessionmaker(
            bind=self.engine,
            autoflush=autofl,
            expire_on_commit=expire_on_commit
        )

    def get_session(self) -> orm.Session:
        return self.session_factory()


def sync_connect_psql(
        auto_commit: bool = False,
        config_: str = config.psql_url,
):
    """
    Декоратор для автоматического подключения к сессии и выхода из сессии Базы Данных.
    Все ошибки, связанные с запросами SQL, декоратор записывает в логи стандартного вывода stdout.

        - при использовании декоратора в функциях либо классах,
        аргумент session должен стоять после всех позиционных аргументов.

    :param auto_commit: По умолчанию False. Для авто-коммита установить True
    :param config_: URL для подключения к БД. По умолчанию используется URL из модуля config
    Если false, то функция вернет своё значение. По умолчанию параметр False
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> typing.Any:
            database_helper = DatabaseHelper(config_)
            with database_helper.get_session() as session:

                try:
                    result = func(*args, session=session, **kwargs)
                    if auto_commit:
                        session.commit()
                    return result
                except Exception as e:
                    session.rollback()
                    raise e
                finally:
                    session.close()

        return wrapper

    return decorator
