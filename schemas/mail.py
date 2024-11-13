from pydantic import BaseModel


class Mail(BaseModel):
    subject: str
    description: str


class MailSend(BaseModel):
    user_mail: str
    subject: str
    description: str
