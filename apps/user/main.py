from .service import registration_user, check_user
from aiohttp.web import Request, json_response
from .schema import RegistrationSerializer
from aiohttp import web


router = web.RouteTableDef()


@router.post('/api/v1/user/registration')
async def registration(request: Request) -> json_response:
    body = RegistrationSerializer(**await request.json())
    await body.model_async_validate()
    await registration_user(body.model_dump())
    return json_response(
        data={"User status": "Success created"},
        status=201
    )


@router.get('/api/v1/user/check/{username}')
async def check_registration(request: Request):
    username = request.match_info.get('username')
    if await check_user(username):
        return json_response(
            data={"Success found": "Пользователь %s зарегистрирован" % username},
            status=200
        )
    else:
        return json_response(
            data={"Not found user": "Пользователь %s не нашелся" % username},
            status=404
        )
