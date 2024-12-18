from jwt.exceptions import PyJWTError
from flask import jsonify, Response


class ErrorCreateJWT(PyJWTError):
    def __init__(self, status_code: int = 400, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg


class BaseErrorCustomJWT(PyJWTError):
    def __init__(self, status_code: int = 400, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if msg is None:
            self.msg = self.default_msg()

    @staticmethod
    def default_msg() -> str:
        ...


class ErrorExpiredToken(BaseErrorCustomJWT):
    @staticmethod
    def default_msg() -> str:
        return "Expired time life token"


class ErrorInvalidToken(BaseErrorCustomJWT):
    @staticmethod
    def default_msg() -> str:
        return "Invalid token"


def error_handler_create_jwt(error: ErrorCreateJWT) -> Response:
    response = jsonify(
        {
            'status': 'error',
            'message': error.msg
        }
    )
    response.status_code = error.status_code
    return response


def error_expired_jwt(error: ErrorExpiredToken) -> Response:
    response = jsonify({"status token": error.msg})
    response.status_code = error.status_code
    return response


def error_invalid_jwt(error: ErrorInvalidToken) -> Response:
    response = jsonify({"status token": error.msg})
    response.status_code = error.status_code
    return response
