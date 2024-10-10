import json
from typing import List

from pydantic import BaseModel, model_validator


class Photo(BaseModel):
    url: str


class Region(BaseModel):
    name: str


class City(BaseModel):
    name: str
    region: Region


class Apartment(BaseModel):
    name: str


class Convenience(BaseModel):
    name:str
    photo: str


class Author(BaseModel):
    id: int
    fullname: str
    phone: str
    mail: str


class ObjectBase(BaseModel):
    name: str
    description: str
    price: int
    area: str
    room_count: int
    bed_count: str
    floor: str
    min_ded: int
    prepayment_percentage: int
    address: str
    #
    # author = relationship("User", back_populates="objects")
    # city = relationship("City", backref="objects")
    # apartment = relationship("Apartment", backref="objects")
    #
    # conveniences = relationship("ObjectConvenience", backref="object")


class ObjectResponse(ObjectBase):
    id: int
    photos: List[str]
    city: City
    apartment: Apartment
    author: Author
    conveniences: List[Convenience]


class ObjectCreate(ObjectBase):
    city_id: int
    apartment_id: int
    convenience: List[int]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

