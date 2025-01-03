from .exception import DuplicateRecordForUser, LimitRecordsForUser, NotFoundRecord
from aiohttp import web
import typing


@web.middleware
async def middleware(request: web.Request, handler: typing.Callable) -> typing.Any:
    try:
        response = await handler(request)
    except (DuplicateRecordForUser, LimitRecordsForUser, NotFoundRecord) as e:
        return web.json_response(data={'record error': e.msg}, status=e.status_code)  # noqa
    else:
        return response
