from fastapi import APIRouter, Depends
from fastapi_mail import MessageSchema, MessageType, FastMail

from schemas.mail import MailSend
from service.mail import mail_conf
from service.security import manager

router = APIRouter(prefix="/email", responses={404: {"description": "Not found"}})


@router.post('/send')
async def send(mail: MailSend, _=Depends(manager)):
    # if not await check_admin(user_auth):
    #     raise Forbidden

    message = MessageSchema(
        subject=mail.subject,
        recipients=[mail.user_mail],
        body=mail.description,
        subtype=MessageType.html)

    fm = FastMail(mail_conf)
    await fm.send_message(message)
    return "successful"
