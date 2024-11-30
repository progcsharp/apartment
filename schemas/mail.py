from typing import List

from pydantic import BaseModel


class Mail(BaseModel):
    subject: str
    description: str
    name: str


class Constructions(BaseModel):
    name: str
    construction: str


class MailOut(BaseModel):
    subject: str
    description: str
    name: str
    slug: str
    constructions: List[Constructions]


class MailSend(BaseModel):
    user_mail: str
    subject: str
    description: str
