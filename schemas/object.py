import json
from typing import List

from pydantic import BaseModel, model_validator


class Photo(BaseModel):
    url: str


class Region(BaseModel):
    id: int
    name: str


class City(BaseModel):
    id: int
    name: str
    region: Region


class Apartment(BaseModel):
    id: int
    name: str


class Convenience(BaseModel):
    id: int
    name:str
    icon: str


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
    child_places: int = 0
    adult_places: int = 0
    floor: str
    min_ded: int
    prepayment_percentage: int
    address: str
    active: bool = False
    letter: str = None
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


class ObjectUpdate(ObjectBase):
    id: int
    city_id: int
    apartment_id: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ObjectUpdatePhotosConvenience(BaseModel):
    removed_photos: List[str] = None
    convenience: List[int]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


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


class ObjectActivate(BaseModel):
    id: int

