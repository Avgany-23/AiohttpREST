from .schemas import AccessSerializer, TokenSerializer
from aiohttp.web import Request, json_response
import apps.auth.service as serv
from aiohttp import web


router = web.RouteTableDef()


@router.post('/api/v1/auth/login')
async def create_access_jwt(requests: Request) -> json_response:
    data = AccessSerializer(**await requests.json()).model_dump()
    user_tokens = await serv.create_jwt_for_user(**data)
    return serv.response_get_token(user_tokens)


@router.post('/api/v1/auth/refresh')
async def update_tokens(requests: Request) -> json_response:
    body = TokenSerializer(**await requests.json()).model_dump()
    new_tokens = serv.refresh_token(**body)
    return serv.response_get_token(new_tokens)


@router.get('/api/v1/auth/status')
async def check_status_token(requests: Request) -> json_response:
    body = TokenSerializer(**await requests.json()).model_dump()
    serv.status_jwt_for_user(**body)
    return json_response(data={'token': "Active"}, status=200)
