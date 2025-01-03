class DuplicateRecordForUser(Exception):
    def __init__(self, status_code: int = 409, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "You already have such a record"


class LimitRecordsForUser(Exception):
    def __init__(self, status_code: int = 403, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "Limit reached"


class NotFoundRecord(Exception):
    def __init__(self, status_code: int = 404, msg: str = None) -> None:
        self.status_code = status_code
        self.msg = msg
        if self.msg is None:
            self.msg = "Record Not Found"
