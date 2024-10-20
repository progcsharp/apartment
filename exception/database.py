from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT


class NotFoundedError(HTTPException):
    def __init__(self) -> None:
        self.status_code = HTTP_404_NOT_FOUND
        self.detail = "not found"


class DependencyConflictError(HTTPException):
    def __init__(self) -> None:
        self.status_code = HTTP_409_CONFLICT
        self.detail = "dependency conflict"
