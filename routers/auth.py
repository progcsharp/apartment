import random
import string

from fastapi import APIRouter, Depends
from fastapi_cache.backends.memory import InMemoryCacheBackend
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_mail import MessageSchema, MessageType, FastMail


from starlette.responses import Response, JSONResponse


from config import mail_conf
from db import redis_cache
from db.engine import get_db
from db.handler.create import create_user
from db.handler.get import get_user
from db.handler.update import update_user_verified
from schemas.user import UserRegister, UserActivate, UserLogin, UserResponse
from service.security import verify_password, manager

router = APIRouter(prefix="/auth", responses={404: {"description": "Not found"}})


@router.get('')
async def get_test(response: Response, cache: InMemoryCacheBackend = Depends(redis_cache), db = Depends(get_db)):
    user = await get_user("q",db)
    print(user)

    return {"users": user}


@router.post('/register', response_model=UserResponse)
async def register(response: Response, user: UserRegister, cache: InMemoryCacheBackend = Depends(redis_cache), db = Depends(get_db)):
    try:
        user_res = await create_user(user, db)
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        # message = MessageSchema(
        #     subject="Fastapi-Mail module",
        #     recipients=[user_res.mail],
        #     body=code,
        #     subtype=MessageType.html)
        await cache.set(user_res.mail, code)
        await cache.expire(user_res.mail, 3600)
        # fm = FastMail(mail_conf)
        # await fm.send_message(message)
    except Exception as e:
        raise

    return user_res


@router.post('/activate', response_model=UserResponse)
async def activate(response: Response, user: UserActivate, cache: InMemoryCacheBackend = Depends(redis_cache), db = Depends(get_db)):
    code = await cache.get(user.mail)
    if code:
        if code == user.code:
            user_res = await update_user_verified(user.mail, db)
        else:
            raise {"user": "Code not sucessful"}
    else:
        raise {"error": "code expire"}
    return user_res


@router.post('/login', response_model=UserResponse)
async def login(response: Response, data: UserLogin, cache: InMemoryCacheBackend = Depends(redis_cache), db = Depends(get_db)):
    username = data.mail
    password = data.password

    user = await get_user(username, db)

    if not user:
        raise InvalidCredentialsException

    if not await verify_password(password, user.password):
        raise
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    print(f"{code}_login")
    await cache.set(f'{user.mail}_login', code)
    await cache.expire(f'{user.mail}_login', 3600)
    return user


@router.post("/login/auth")
async def login_auth(response: Response, user: UserActivate, cache: InMemoryCacheBackend = Depends(redis_cache), db = Depends(get_db)):
    user_res = await get_user(user.mail, db)
    if not user_res:
        return JSONResponse(status_code=200, content={"user": "not found"})
    code = await cache.get(f'{user.mail}_login')
    if code != user.code:
        return False

    token = manager.create_access_token(
        data=dict(sub=user_res.mail)
    )
    manager.set_cookie(response, token)
    return user_res


