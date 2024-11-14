from pydantic import BaseModel


class Mail(BaseModel):
    subject: str
    description: str
    name: str


class MailOut(BaseModel):
    subject: str
    description: str
    name: str
    slug: str


class MailSend(BaseModel):
    user_mail: str
    subject: str
    description: str
