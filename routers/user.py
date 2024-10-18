from fastapi import APIRouter, Depends, Body

from db.engine import get_db
from db.handler.create import create_user
from db.handler.delete import delete_user
from db.handler.get import get_user_by_id, get_all_users, get_user
from db.handler.update import update_user_activate, update_user_tariff_activate, update_user_password
from permission.is_admin import check_admin
from schemas.user import UserResponse, UserResponseList, UserRegister, UserTariffActivate, UserActivate, \
    UserResetPassword
from service.security import manager

router = APIRouter(prefix="/user", responses={404: {"description": "Not found"}})


@router.get("/id/", response_model=UserResponse)
async def get(id: int, db=Depends(get_db)):
    # if not await check_admin(user_auth):
    #     raise user_auth= Depends(manager),
    user = await get_user_by_id(id, db)
    return user


@router.get("/all/", response_model=UserResponseList)
async def get_all(db=Depends(get_db)):
    user = await get_all_users(db)
    return {"users":user}


@router.get("/profile", response_model=UserResponse)
async def profile(user_auth=Depends(manager), db=Depends(get_db)):
    user = await get_user(user_auth.mail, db)
    return user


@router.put("/activate", response_model=UserResponse)
async def activate(user_data: UserActivate,  db=Depends(get_db)):
    # if not await check_admin(user_auth):
    #     raise user_auth=Depends(manager),
    user = await update_user_activate(user_data, db)
    return user


@router.put("/tariff/activate", response_model=UserResponse)
async def tariff_active(user_data: UserTariffActivate, db=Depends(get_db)):
    user = await update_user_tariff_activate(user_data, db)
    return user


@router.put("/reset/password", response_model=UserResponse)
async def reset_password(user_data: UserResetPassword, user_id: int, db=Depends(get_db)):
    user = await update_user_password(user_data, user_id, db)
    return user


@router.post("/create", response_model=UserResponse)
async def create(user_data: UserRegister, db=Depends(get_db)):
    user = await create_user(user_data, db)
    return user


@router.delete('/delete')
async def delete(id_user: int, db=Depends(get_db)):
    user = await delete_user(id_user, db)
    return user

