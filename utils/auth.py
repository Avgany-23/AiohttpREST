from apps.auth.exceptions import ErrorInvalidToken, ErrorExpiredToken
from apps.auth.config import jwt_conf
from aiohttp import web
import typing
import jwt


# Список endpoints, требующих аутентификацию. Если элемент состоит из строки, то аутентификация будет требоваться на
# все методы указанного url. Если состоит из кортежа, то во втором элементе указывается список метод,
# на которые нужна аутентификация.
# Знак $ означает, что маршрут должен начинаться с указанного названия
auth_list = [
    ('/api/v1/record', ['PUT', 'POST']),
    ('$/api/v1/record', ['DELETE', 'PATCH']),
    '/api/v1/my_records',
]


class NotFoundTokenJWT(jwt.PyJWTError):
    def __init__(self, status_code: int = 401, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = {"Not authentication": "Token JWT not found"}


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


def parse_urls(path: str, method: str) -> bool:
    """
    Функция проверяет, принадлежит ли путь path и method списку auth_list
    :param path: путь запроса
    :param method: метод запроса
    :return: bool
    """
    for p in auth_list:
        result_path = p
        result_method = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS']

        if isinstance(result_path, str):
            ...

        elif isinstance(result_path, (list, tuple)):
            if len(result_path) != 2:
                raise AttributeError('Аргумент path должен содержать 2 элемента, но не %s' % len(path))
            if method not in result_method:
                raise AttributeError('Метод должен принадлежать списку %s' % result_method)
            result_path, result_method = p
            if not isinstance(result_method, (list, tuple)):
                raise AttributeError('Второй аргумент должен быть списком или кортежем')

        else:
            raise TypeError('Параметр path должен быть типом str, tuple или list, но не %s' % type(result_path))

        if result_path[0] == "$":
            if path.startswith(result_path[1:]) and method in result_method:
                return True
        elif result_path == path and method in result_method:
            return True

    return False


def finder_from_header_jwt(headers: dict) -> dict:
    access_jwt = headers.get("Authorization")
    if access_jwt is None:
        raise NotFoundTokenJWT

    access_jwt = access_jwt.replace("Bearer ", "")
    initial = UserRefreshJWT(token=access_jwt)
    token = initial.check_token()
    if initial.check_refresh_token():
        raise ErrorInvalidToken
    return token


def auth(request: web.Request) -> web.Request:
    """
    Аутентификация пользователя проходит, если передано ключ-значение token: <token> и переданный токен является типом
    access, если токен корректный и если срок жизни токена не истек.
    """
    path = request.path
    method = request.method
    request.user_id = None
    if not parse_urls(path, method):
        return request

    token = finder_from_header_jwt(dict(request.headers))
    request.user_id = token.get('user_id')

    return request
