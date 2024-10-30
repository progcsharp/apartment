from typing import List

from pydantic import BaseModel


class RegionBase(BaseModel):
    name: str


class RegionCreate(RegionBase):
    pass


class CityInRegion(BaseModel):
    id: int
    name: str


class RegionResponse(BaseModel):
    id: int
    name: str
    cities: List[CityInRegion] = []
    object_count: int


class RegionCreateResponse(BaseModel):
    id: int
    name: str


class RegionResponseList(BaseModel):
    regions: List[RegionResponse]


