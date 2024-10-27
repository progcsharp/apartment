from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_406_NOT_ACCEPTABLE


class Forbidden(HTTPException):
    def __init__(self) -> None:
        self.status_code = HTTP_403_FORBIDDEN
        self.detail = "Access denied"


class NoVerifyPWD(HTTPException):
    def __init__(self):
        self.status_code = HTTP_406_NOT_ACCEPTABLE
        self.detail = "No verify password"


class NoVerifyCode(HTTPException):
    def __init__(self):
        self.status_code = HTTP_406_NOT_ACCEPTABLE
        self.detail = "No verify code"


class CodeExpire(HTTPException):
    def __init__(self):
        self.status_code = HTTP_406_NOT_ACCEPTABLE
        self.detail = "Code expire"
