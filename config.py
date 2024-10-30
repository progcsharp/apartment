import configparser

from fastapi_mail import ConnectionConfig

settings = configparser.ConfigParser()
settings.read('settings.ini')

mail_conf = ConnectionConfig(
    MAIL_USERNAME = "fonror@mail.ru",
    MAIL_PASSWORD = "964dCGrEXvP3BcnwaBkV",
    MAIL_FROM = "fonror@mail.ru",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.mail.ru",
    MAIL_FROM_NAME="StayFlex",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False)
