from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
import sqlalchemy as sq
from db import basic


class User(basic):
    __tablename__ = 'user'  # noqa

    id: Mapped[Annotated[int, mapped_column(sq.BigInteger, primary_key=True)]]
    username: Mapped[str] = mapped_column(sq.VARCHAR(50), unique=True)
    email: Mapped[str | None] = mapped_column(sq.VARCHAR(50), nullable=True)
    password: Mapped[str] = mapped_column(sq.TEXT)

    record: Mapped[list['Record']] = relationship(back_populates='user', lazy='joined')  # noqa

    def __str__(self):
        return self.username
