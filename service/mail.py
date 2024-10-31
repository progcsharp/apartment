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


authorization = {"Theme": "Двухфакторная авторизация",
                 "description": "Ваш код авторизации (?code)"}

register = {"Theme": "Регистрация",
                 "description": "Поздравляем вы зарегестрировали на портале StayFlex. Мы вас уведомим когда ваш аккаунт будет активирован"}
