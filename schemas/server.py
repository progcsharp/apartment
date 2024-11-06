import json

from pydantic import BaseModel, model_validator


class ServerBase(BaseModel):
    name: str
    container_name: str


class ServerResponse(ServerBase):
    id: int


class ServerCreate(ServerBase):

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
