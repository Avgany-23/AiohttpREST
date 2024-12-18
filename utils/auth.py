from apps.auth.exception import ErrorInvalidToken
from apps.auth.service import UserRefreshJWT
from utils.exception import NotFoundTokenJWT
from flask import Request, request as request_


def auth(request: Request) -> None:
    """
    Аутентификация пользователя проходит, если передано ключ-значение token: <token> и переданный токен является типом
    access, если токен корректный и если срок жизни токена не истек.
    """
    access_jwt = request.headers.get("Authorization")
    if access_jwt is None:
        raise NotFoundTokenJWT
    access_jwt = access_jwt.replace("Bearer ", "")
    initial = UserRefreshJWT(token=access_jwt)
    token = initial.check_token()
    if initial.check_refresh_token():
        raise ErrorInvalidToken
    request_.user_id = token.get('user_id')
