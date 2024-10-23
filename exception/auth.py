from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN


class Forbidden(HTTPException):
    def __init__(self) -> None:
        self.status_code = HTTP_403_FORBIDDEN
        self.detail = "Access denied"

