from fastapi import FastAPI, Depends

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.memory import CACHE_KEY, InMemoryCacheBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.middleware.cors import CORSMiddleware

from db import User
from db.engine import DBContext
from service.security import manager

from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.region import router as region_router
from routers.city import router as city_router
from routers.apartment import router as apartment_router
from routers.convenience import router as convenience_router
from routers.object import router as object_router
from routers.client import router as client_router
from routers.reservation import router as reservation_router
from routers.tariff import router as tariff_router
from routers.hashtag import router as hashtag_router
from routers.admin import router as admin_router
from routers.mail import router as mail_router


app = FastAPI(debug=False)


origins = ["http://37.140.198.195:8000", "https://stayflex.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=tariff_router)
app.include_router(router=region_router)
app.include_router(router=city_router)
app.include_router(router=apartment_router)
app.include_router(router=convenience_router)
app.include_router(router=object_router)
app.include_router(router=client_router)
app.include_router(router=reservation_router)
app.include_router(router=hashtag_router)
app.include_router(router=admin_router)
app.include_router(router=mail_router)


@manager.user_loader()
async def user_loader(mail, db: async_sessionmaker = None):
    if db is None:
        # user = await get_user(user, DBContext)
        with DBContext() as db:
            query = select(User).where(User.mail == mail)
            result = await db.execute(query)
            user = result.scalar_one_or_none()

            if user is None:
                print(f"Пользователь с email {user} не найден.")
                return None
            print(user.mail)
            return user
    # user = await get_user(user, db)
    # return user


@app.on_event('startup')
async def on_startup() -> None:
    rc = InMemoryCacheBackend()
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
