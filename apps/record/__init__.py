from .main import app as router
from .models import Record as ModelRecord

__all__ = (
    'router',
    'ModelRecord',
)
