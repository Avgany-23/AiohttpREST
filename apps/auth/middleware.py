from .exceptions import BaseErrorCustomJWT, ErrorCreateJWT
from aiohttp import web
import typing


@web.middleware
async def middleware(request: web.Request, handler: typing.Callable) -> typing.Any:
    try:
        response = await handler(request)
    except (BaseErrorCustomJWT, ErrorCreateJWT) as e:
        return web.json_response(data={'token error': e.msg}, status=e.status_code)  # noqa
    else:
        return response
