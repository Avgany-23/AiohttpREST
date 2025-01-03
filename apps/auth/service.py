from .exceptions import ErrorCreateJWT, ErrorInvalidToken, ErrorExpiredToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, select
from utils import check_password
from apps.user import ModelUser
from .config import jwt_conf
from aiohttp import web
import collections
import typing
import time
import jwt
import db


@db.connect_psql()
async def get_user_to_db(username: str, password: str, session: AsyncSession) -> Row | None:
    stmt = select(ModelUser).filter_by(username=username)
    result = (await session.execute(stmt)).scalar()
    if result and check_password(password.encode(), result.password.encode()):  # noqa
        return result


class UserCreateJWT:
    """Класс для создания access и refresh JWT токенов"""

    Tokens = collections.namedtuple('Tokens', ['access', 'refresh'])

    def __init__(self, user_id: str, username: str):
        self.user_id = user_id
        self.username = username

    def create_jwt(self) -> Tokens | ErrorCreateJWT:
        payload = {"user_id": self.user_id, "user_name": self.username}
        return self.Tokens(
            access=self.create_jwt_token(payload, access=True),
            refresh=self.create_jwt_token(payload, access=False)
        )

    @staticmethod
    def create_jwt_token(data: dict, access: bool = True) -> str:
        exp = time.time()
        if access:
            data_token = {"exp": exp + jwt_conf.ACCESS_TOKEN_LIFETIME.total_seconds()}
        else:
            data_token = {"exp": exp + jwt_conf.REFRESH_TOKEN_LIFETIME.total_seconds(), "refresh": True}
        data.update(**data_token)
        return jwt.encode(data, jwt_conf.SECRET_KEY, algorithm=jwt_conf.ALGORITHM)


class UserRefreshJWT:
    """Класс для проверки JWT токенов"""

    def __init__(self, token: str) -> None:
        """
        :param token: JWT токен
        """
        self.token = token

    def check_token(self) -> typing.Any | jwt.ExpiredSignatureError | jwt.InvalidTokenError:
        """Метод проверяет JWT self.token на корректность и актуальность"""
        try:
            token = self.get_user_from_token()
        except jwt.ExpiredSignatureError:
            raise ErrorExpiredToken
        except jwt.InvalidTokenError:
            raise ErrorInvalidToken
        return token

    def check_refresh_token(self) -> bool:
        """
        Метод проверяет токен на статус refresh JWT
        :return: True, если токен типа refresh, False в ином случае
        """
        token = self.check_token()
        if token.get('refresh', None):
            return True
        return False

    def get_user_from_token(self) -> dict:
        payload = jwt.decode(self.token, jwt_conf.SECRET_KEY, algorithms=[jwt_conf.ALGORITHM])
        return payload


def create_jwt_token(user_id: str, username: str) -> UserCreateJWT.Tokens:
    """Функция для создания JWT токенов"""
    initial = UserCreateJWT(user_id=user_id, username=username)
    return initial.create_jwt()


async def create_jwt_for_user(username: str, password: str) -> UserCreateJWT.Tokens | ErrorCreateJWT:
    """Функция для создания JWT токенов для пользователя"""
    user = await get_user_to_db(username=username, password=password)
    if user:
        return create_jwt_token(user_id=user.id, username=user.username)
    raise ErrorCreateJWT(msg="Токены не были созданы. Получен неверный логин/пароль.")


def status_jwt_for_user(token: str) -> typing.Any | jwt.ExpiredSignatureError | jwt.InvalidTokenError:
    """Функция для проверки JWT токена"""
    initial = UserRefreshJWT(token=token)
    return initial.check_token()


def refresh_token(token: str) -> UserCreateJWT.Tokens | jwt.ExpiredSignatureError | jwt.InvalidTokenError:
    """
    Функция для обновления JWT токенов
    :param token: access токен
    :return: Два новых токена, если получен актуальный и верный refresh JWT
    """
    initial = UserRefreshJWT(token=token)
    if initial.check_refresh_token():
        old_refresh_token = initial.check_token()
        user_id, username = old_refresh_token.get('user_id'), old_refresh_token.get('user_name')
        return create_jwt_token(user_id=user_id, username=username)
    raise ErrorInvalidToken


def response_get_token(tokens: UserCreateJWT.Tokens) -> web.Response:
    response = web.json_response(
        {
            'access': tokens.access,
            'refresh': tokens.refresh
        },
        status=201
    )
    return response
