from typing import List

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    region_id: int


class RegionOfCity(BaseModel):
    id: int
    name: str


class CityResponse(CityBase):
    id: int
    region: RegionOfCity


class CityResponseList(BaseModel):
    cities: List[CityResponse]

