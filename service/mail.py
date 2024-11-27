import json
import re

from fastapi_mail import ConnectionConfig

mail_conf = ConnectionConfig(
    MAIL_USERNAME = "fonror@mail.ru",
    MAIL_PASSWORD = "964dCGrEXvP3BcnwaBkV",
    MAIL_FROM = "fonror@mail.ru",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.mail.ru",
    MAIL_FROM_NAME="StayFlex",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False)

with open('mail.json', 'r') as f:
    data = json.load(f)

authorization = data['authorization']

register = data['register']

activate = data['activate']

deactivate = data['deactivate']

reservation = data['reservation']


def check_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))

