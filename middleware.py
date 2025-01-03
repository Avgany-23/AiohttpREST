from apps import auth_middleware, record_middleware
from utils.auth import auth, NotFoundTokenJWT
from utils import ForbiddenError
from aiohttp import web
import pydantic
import typing
import json


# Список отдельных middleware с приложений
apps_middleware = [
    auth_middleware,
    record_middleware
]


@web.middleware
async def middleware_auth(request: web.Request, handler: typing.Callable) -> typing.Any:
    """Middleware для аутентификации и прав доступа"""
    try:
        auth(request)
        response = await handler(request)
    except NotFoundTokenJWT as e:
        return web.json_response(data=e.msg, status=e.status_code)
    except ForbiddenError as e:
        return web.json_response(data=e.msg, status=e.status_code)
    return response


@web.middleware
async def middleware_pydantic_validation(request: web.Request, handler: typing.Callable) -> typing.Any:
    """Middleware для обработки исключений валидации pydantic"""
    try:
        response = await handler(request)
    except pydantic.ValidationError as e:
        return web.json_response(data=json.loads(e.json()), status=400)
    else:
        return response


@web.middleware
async def middleware_json_error_encoder(request: web.Request, handler: typing.Callable) -> typing.Any:
    """Middleware для обработки исключений json кодировки. В частности обратного слэша."""
    try:
        response = await handler(request)
    except json.decoder.JSONDecodeError as e:
        error_msg = '%s: line %d column %d (char %d)' % (e.msg, e.lineno, e.colno, e.pos)
        return web.json_response(data={'json encoder error': error_msg}, status=400)
    else:
        return response
