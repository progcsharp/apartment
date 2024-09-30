from datetime import date
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    mail: str


class UserLogin(UserBase):
    password: str


class UserRegister(UserBase):
    fullname: str
    phone: str
    password: str
    tarif: str = "standart"
    is_active: bool = False
    is_verified: bool = False
    is_admin: bool = False
    balance: int = 0
    date_before: date = date.today()


class UserActivate(UserBase):
    code: str


class UserResponse(UserBase):
    id: int
    fullname: str
    phone: str
    tarif: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    balance: int
    date_before: date


class UserResponseList(BaseModel):
    users: List[UserResponse]


