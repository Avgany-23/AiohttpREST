from jwt.exceptions import PyJWTError


class NotFoundTokenJWT(PyJWTError):
    def __init__(self, status_code: int = 401, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "Token JWT not found"


class ForbiddenError(Exception):
    def __init__(self, msg: str = None) -> None:
        self.status_code = 403
        self.msg = msg
        if self.msg is None:
            self.msg = {"forbidden": "Недостаточно прав"}
