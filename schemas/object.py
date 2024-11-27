import json
from datetime import date
from typing import List, Union

from pydantic import BaseModel, model_validator


def remove_field(field_name: str):
    def decorator(cls):
        cls._remove_field = field_name
        return cls
    return decorator

    @classmethod
    def _remove_field(cls):
        if hasattr(cls(), cls._remove_field):
            delattr(cls(), cls._remove_field)


class Photo(BaseModel):
    url: str


class Region(BaseModel):
    id: int
    name: str


class Reservation(BaseModel):
    id: int
    start_date: date
    end_date: date


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


class Hashtag(BaseModel):
    id: int
    name: str


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
    letter: str = None


@remove_field('letter')
class PublicObject(ObjectResponse):
    approve_reservation: Union[List[Reservation], None]
    hashtags: List[Hashtag]


class ObjectUpdate(ObjectBase):
    id: int
    city_id: int
    apartment_id: int
    letter: str = None

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
    hashtags: List[int] = []
    letter: str = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ObjectActivate(BaseModel):
    id: int

