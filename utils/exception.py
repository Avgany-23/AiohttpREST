from flask import jsonify, Response
from pydantic_core import ValidationError
from jwt.exceptions import PyJWTError


def pydantic_error_handler(error: ValidationError) -> Response:
    message = error.errors()[0]
    message = {
        'type': message['type'],
        'loc': message['loc'],
        'message': message['msg']
    }

    response = jsonify(
        {
            'status': 'error',
            'message': message
        }
    )
    response.status_code = 400
    return response


class NotFoundTokenJWT(PyJWTError):
    def __init__(self, status_code: int = 401, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "Token JWT not found"


def error_not_found_access_jwt(error: NotFoundTokenJWT) -> Response:
    response = jsonify({"error token": error.msg})
    response.status_code = error.status_code
    return response


class ForbiddenError(Exception):
    def __init__(self, msg: str = None) -> None:
        self.status_code = 403
        self.msg = msg
        if self.msg is None:
            self.msg = "Недостаточно прав"


def error_forbidden(error: ForbiddenError) -> Response:
    response = jsonify({"error": error.msg})
    response.status_code = error.status_code
    return response
