from typing import List

from pydantic import BaseModel


class ApartmentBase(BaseModel):
    name: str


class ApartmentCreate(ApartmentBase):
    pass


class ApartmentResponse(ApartmentBase):
    id: int


class ApartmentResponseList(BaseModel):
    id: int
    name: str
    object_count: int
