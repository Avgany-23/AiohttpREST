from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils import hash_password
from db import connect_psql
from .models import User


@connect_psql(auto_commit=True)
async def registration_user(data: dict, session: AsyncSession) -> None:
    password = hash_password(data.pop('password').encode())
    user = User(**data, password=password.decode())
    session.add(user)
    await session.commit()


@connect_psql()
async def check_user(username: str, session: AsyncSession) -> bool:
    stmt = select(User).filter_by(username=username)
    user = await session.execute(stmt)
    if user.scalar():
        return True
    return False
