from typing import List

from fastapi import UploadFile, File
from pydantic import BaseModel


class ConvenienceBase(BaseModel):
    name: str


class ConvenienceResponse(ConvenienceBase):
    id: int
    photo: str


class ConvenienceResponseList(ConvenienceBase):
    convenience: List[ConvenienceResponse]


class ConvenienceCreate(ConvenienceBase):
    pass
