from .auth import router as rout_auth
from .record import router as rout_record
from .user import router as rout_user


__all__ = (
    'rout_auth',
    'rout_record',
    'rout_user'
)
