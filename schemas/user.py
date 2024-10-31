from datetime import date
from typing import List, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    mail: str


class UserLogin(UserBase):
    password: str


class Tariff(BaseModel):
    id: int
    name: str


class UserRegister(UserBase):
    fullname: str
    phone: str
    password: str
    tariff_id: int = None


class UserCreate(UserBase):
    fullname: str
    phone: str
    password: str
    is_active: bool = False
    is_admin: bool = False
    balance: int = 0
    tariff_id: int = None


class UserActivateCode(UserBase):
    code: str


class UserResponse(UserBase):
    id: int
    fullname: str
    phone: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    balance: int
    date_before: date
    tariff: Union[Tariff, None]


class UserRegisterResponse(BaseModel):
    id: int
    fullname: str
    phone: str
    mail: str


class UserResponseList(BaseModel):
    id: int
    fullname: str
    is_active: bool
    date_before: date
    object_count: int


class UserTariffActivate(BaseModel):
    user_id: int
    tariff_id: int
    balance: int


class UserResetPassword(BaseModel):
    id: int
    new_password: str


class UserActivate(BaseModel):
    id: int


class UserUpdateAdmin(BaseModel):
    id: int
    fullname: str
    phone: str
    mail: str


class UserUpdate(BaseModel):
    fullname: str
    phone: str
