from flask import Response, jsonify


class DuplicateRecordForUser(Exception):
    def __init__(self, status_code: int = 409, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "You already have such a record"


def error_duplicate_record(error: DuplicateRecordForUser) -> Response:
    response = jsonify({"error": error.msg})
    response.status_code = error.status_code
    return response


class LimitRecordsForUser(Exception):
    def __init__(self, status_code: int = 403, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "Limit reached"


def error_limit_record(error: LimitRecordsForUser) -> Response:
    response = jsonify({"error": error.msg})
    response.status_code = error.status_code
    return response
