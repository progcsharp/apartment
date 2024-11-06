import json

from pydantic import BaseModel, model_validator


class ServerBase(BaseModel):
    name: str
    container_name: str


class ServerResponse(ServerBase):
    id: int
    default: bool


class ServerCreate(ServerBase):

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ServerUpdate(ServerBase):
    id: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

