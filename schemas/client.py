import json

from pydantic import BaseModel, model_validator


class ClientBase(BaseModel):
    fullname: str
    reiting: float
    phone: str
    email: str


class ClientCreate(ClientBase):

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ClientResponse(ClientBase):
    id: int
