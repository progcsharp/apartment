from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    is_admin: bool
    fullname: str


class LogsOut(BaseModel):
    user: User
    description: str
    created_at: datetime
