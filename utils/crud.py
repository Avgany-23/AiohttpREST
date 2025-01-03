from sqlalchemy import RowMapping, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Any
import sqlalchemy as sql
import abc
import db


class BaseRequest(abc.ABC):
    """
    Базовый класс для запросов к моделям. Для работы необходимо указать таблицу table,
    к которой будут идти запросы.

    Все методы принимают позиционный аргумент session, при использовании данных методов
    данный аргумент подставится автоматически за счет декоратор.
    Session должен стоять после позиционных аргументов
    """

    @property
    @abc.abstractmethod
    def table(self):
        """Свойство класса - модель sqlalchemy, к которой осуществляются запросы"""
        pass

    @db.connect_psql()
    async def get_all(self, session: AsyncSession, limit: int = None) -> Sequence[RowMapping]:
        """
        Метод выдает итератор со всеми записями
        :param session: объект сессии psql
        :param limit: количество записей
        :return: iter
        """
        stmt = sql.select(sql.text('*')).select_from(self.table).limit(limit)
        result = (await session.execute(stmt)).unique()
        return result.mappings().all()

    @db.connect_psql()
    async def get_several(self, session: AsyncSession, **kwargs) -> Sequence[RowMapping]:
        """
        Метод выдает все записи по фильтру(ам) из kwargs
        :param session: объект сессии psql
        :param kwargs: словарь с фильтрами
        :return: запись запроса либо None
        """
        stmt = sql.select(sql.text('*')).select_from(self.table).filter_by(**kwargs)
        result = (await session.execute(stmt)).unique()
        return result.mappings().all()

    @db.connect_psql()
    async def get_one(self, session: AsyncSession, **kwargs) -> sql.RowMapping:
        """
        Метод выдает первую запись по фильтру(ам) из kwargs
        :param session: объект сессии psql
        :param kwargs: словарь с фильтрами
        :return: запись запроса либо None
        """
        stmt = sql.select(sql.text('*')).select_from(self.table).filter_by(**kwargs)
        result = (await session.execute(stmt)).unique()
        return result.mappings().first()

    @db.connect_psql(auto_commit=True)
    async def create_one(self, session: AsyncSession, **kwargs) -> None:
        """
        Создание записи со значениями kwargs. Метод вернет True, если запись создастся
        :param session: объект сессии psql
        :param kwargs: словарь с новыми значениями записи
        :return: True, если создание прошло успешно.
        """
        session.add(self.table(**kwargs))

    @db.connect_psql(auto_commit=True)
    async def update_record(self, new_value: dict[str, str], session: AsyncSession, **kwargs) -> CursorResult[Any]:
        """
        Обновление записи(сей). Обновляет по фильтрам из kwargs.
        :param new_value: Словарь с новыми значениями
        :param session: объект сессии psql
        :param kwargs: фильтры
        :return: True, если обновление прошло успешно.
        """
        stmt = sql.update(self.table).filter_by(**kwargs).values(new_value)
        return await session.execute(stmt)

    @db.connect_psql(auto_commit=True)
    async def delete_record(self, session: AsyncSession, **kwargs) -> None:
        """
        Создание записи(сей) со значениями kwargs. Вернет количество удаленных записей
        :param session: объект сессии psql
        :param kwargs: словарь с фильтрами для нахождения удаляемых записей
        :return: True, если удаление прошло успешно.
        """
        await session.execute(sql.delete(self.table).filter_by(**kwargs))
