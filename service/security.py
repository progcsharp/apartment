from datetime import timedelta

from fastapi_login import LoginManager
from passlib.context import CryptContext
import passlib.handlers.bcrypt

from config import settings as config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


manager = LoginManager(config['AUTH']['SECRET'], config['AUTH']['PATH'],
                       use_cookie=True,
                       cookie_name=config['AUTH']['COOKIE_NAME'],
                       use_header=False,
                       default_expiry=timedelta(days=1)
                       )


async def hash_password(plaintext: str):
    return pwd_context.hash(plaintext)


async def verify_password(plaintext: str, hashed: str):
    return pwd_context.verify(plaintext, hashed)
