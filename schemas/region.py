from typing import List, Union

from pydantic import BaseModel


class RegionBase(BaseModel):
    name: str


class RegionCreate(RegionBase):
    server_id: int


class CityInRegion(BaseModel):
    id: int
    name: str


class Server(BaseModel):
    id: int
    name: str


class RegionResponse(BaseModel):
    id: int
    name: str
    cities: List[CityInRegion] = []
    object_count: int
    servers: Union[Server, None]


class RegionCreateResponse(BaseModel):
    id: int
    name: str


class RegionResponseList(BaseModel):
    regions: List[RegionResponse]


