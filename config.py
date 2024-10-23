import configparser

from fastapi_mail import ConnectionConfig

settings = configparser.ConfigParser()
settings.read('settings.ini')

mail_conf = ConnectionConfig(
    MAIL_USERNAME = "fonror@mail.ru",
    MAIL_PASSWORD = "964dCGrEXvP3BcnwaBkV",
    MAIL_FROM = "fonror@mail.ru",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.mail.ru",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
