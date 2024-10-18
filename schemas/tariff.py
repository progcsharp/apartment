import json

from pydantic import BaseModel, model_validator


class TariffBase(BaseModel):
    name: str
    daily_price: int
    object_count: int
    description: str


class TariffCreate(TariffBase):

    icon: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class TariffResponse(TariffBase):
    id: int
    icon: str


class TariffUpdate(TariffBase):
    id: int
    icon: str
