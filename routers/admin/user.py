from typing import List

from fastapi import APIRouter, Depends, Body

from db.engine import get_db
from db.handler.create import create_user
from db.handler.delete import delete_user
from db.handler.get import get_user_by_id, get_all_users, get_user
from db.handler.update import update_user_activate, update_user_tariff_activate, update_user_password, update_user
from permission.is_admin import check_admin
from schemas.user import UserResponse, UserTariffActivate, UserActivate, \
    UserResetPassword, UserUpdateAdmin, UserUpdate, UserCreate
from service.security import manager

router = APIRouter(prefix="/user", responses={404: {"description": "Not found"}})


#admin
@router.get("/id/{user_id}", response_model=UserResponse)
async def get(user_id: int, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await get_user_by_id(user_id, db)
    return user


#admin
@router.get("/all/", response_model=List[UserResponse])
async def get_all(db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await get_all_users(db)
    return user

#admin
@router.put("/activate", response_model=UserResponse)
async def activate(user_data: UserActivate,  db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await update_user_activate(user_data, db)
    return user

#admin
@router.put("/tariff/activate", response_model=UserResponse)
async def tariff_active(user_data: UserTariffActivate, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await update_user_tariff_activate(user_data, db)
    return user

#admin
@router.put("/reset/password", response_model=UserResponse)
async def reset_password(user_data: UserResetPassword, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await update_user_password(user_data, user_data.id, db)
    return user


# @router.put("/update", response_model=UserResponse)
# async def update(user_data: UserUpdate,user_auth=Depends(manager), db=Depends(get_db)):
#     user_data.id = user_auth.id
#     user = await update_user(user_data, db)
#     return user

#admin
@router.put("/update", response_model=UserResponse)
async def update(user_data: UserUpdateAdmin, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await update_user(user_data, db)
    return user

#admin
@router.post("/create", response_model=UserResponse)
async def create(user_data: UserCreate, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await create_user(user_data, db)
    return user

#admin
@router.delete('/delete/{user_id}')
async def delete(user_id: int, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    user = await delete_user(user_id, db)
    return user
