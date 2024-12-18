from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
import sqlalchemy as sq
from db import basic
import datetime


class Record(basic):
    __tablename__ = 'record'  # noqa

    id: Mapped[Annotated[int, mapped_column(sq.BigInteger, primary_key=True)]]
    title: Mapped[str] = mapped_column(sq.VARCHAR(50))
    description: Mapped[str | None]
    date_created: Mapped[datetime.datetime] = mapped_column(
        sq.TIMESTAMP, default=datetime.datetime.now(), server_default=sq.func.now()
    )
    owner: Mapped[int] = mapped_column(sq.BigInteger, sq.ForeignKey('user.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='record', lazy='joined')  # noqa

    __table_args__ = (
        sq.UniqueConstraint('title', 'owner', name='unique_title_owner'),
    )

    def __str__(self):
        return self.title
