from aiohttp import web
from apps import routers
import middleware


app = web.Application(
    middlewares=middleware.apps_middleware + [
        middleware.middleware_pydantic_validation,
        middleware.middleware_auth,
        middleware.middleware_json_error_encoder,
    ]
)
for rout in routers:
    app.add_routes(rout)
