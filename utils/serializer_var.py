from typing import TypeVar, Union, Any
import pydantic_core


ReturnSerializer = TypeVar("ReturnSerializer", bound=Union[pydantic_core.PydanticCustomError, Any])
