from flask import request, Response
from utils.auth import auth


def before_request_auth():
    """
    На все запросы по адресу, начинающегося с /auth/user/ идет проверка аутентификации пользователя.
    """
    if request.path.startswith('api/v1/auth/user/'):
        auth(request)


def after_request_base(response: Response):
    return response


class SessionMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Низкоуровневый middleware
        # before
        response = self.app(environ, start_response)
        # after
        return response
