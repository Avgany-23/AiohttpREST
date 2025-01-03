from .record import router as record_rout, middleware as record_middleware
from .auth import router as auth_rout, middleware as auth_middleware
from .user import router as user_rout


routers = [
    auth_rout,
    user_rout,
    record_rout
]

__all__ = (
    'auth_middleware',
    'record_middleware',
    'routers',
)
