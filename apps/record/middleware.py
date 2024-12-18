from utils.auth import auth
from flask import request


def before_request_auth():
    """
    На все запросы по адресу /record (кроме record GET) идет проверка аутентификации пользователя.
    Аутентификация проходит, если передано ключ-значение token: <token> и переданный токен является типом access, если
    токен корректный и если срок жизни токена не истек.
    """
    if (request.path == '/api/v1/record' and request.method != 'GET') or request.path == '/api/v1/record/my_records':
        auth(request)
