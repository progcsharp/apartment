import json

from fastapi import APIRouter, Depends
from fastapi_mail import MessageSchema, MessageType, FastMail

from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.mail import Mail, MailSend
from service.mail import mail_conf
from service.security import manager

router = APIRouter(prefix="/email", responses={404: {"description": "Not found"}})


@router.get('/all')
async def all(user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden

    with open('mail.json', 'r') as f:
        data = json.load(f)

    return data


@router.put('/{name}')
async def edit(name: str, email: Mail, user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden

    with open('mail.json', 'r') as f:
        data = json.load(f)

    data[name]['subject'] = email.subject
    data[name]['description'] = email.description

    with open('mail.json', 'w') as file:
        json.dump(data, file, indent=2)

    return True


@router.post('/send')
async def send(mail: MailSend, user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden

    message = MessageSchema(
        subject=mail.subject,
        recipients=[mail.user_mail],
        body=mail.description,
        subtype=MessageType.html)

    fm = FastMail(mail_conf)
    await fm.send_message(message)

