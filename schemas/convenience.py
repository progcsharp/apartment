import json
from typing import List

from fastapi import UploadFile, File
from pydantic import BaseModel, model_validator


class ConvenienceBase(BaseModel):
    name: str


class ConvenienceResponse(ConvenienceBase):
    id: int
    icon: str


class ConvenienceResponseList(ConvenienceBase):
    icon: str
    object_count: int


class ConvenienceCreate(ConvenienceBase):
    icon: str


    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value