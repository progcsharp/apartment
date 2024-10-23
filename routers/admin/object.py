from typing import Optional, List

from fastapi import APIRouter, Body, UploadFile, File, Depends

from db.engine import get_db
from db.handler.create import create_object
from db.handler.delete import delete_object
from db.handler.get import get_all_object, get_by_id_object, get_object_by_user_id
from db.handler.update import update_object_activate
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.object import ObjectCreate, ObjectResponse, ObjectActivate
from service.security import manager

router = APIRouter(prefix="/object", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ObjectResponse])
async def get_all(db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden

    objects = await get_all_object(db)
    return objects


@router.get("/id/{object_id}", response_model=ObjectResponse)
async def get(object_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    objects = await get_by_id_object(object_id, db)
    return objects


@router.get("/userid/{user_id}", response_model=List[ObjectResponse])
async def get(user_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    objects = await get_object_by_user_id(user_id, db)
    return objects


@router.put("/activate", response_model=ObjectResponse)
async def activate(object_id: ObjectActivate, user_auth=Depends(manager), db=Depends(get_db)):#user_auth=Depends(manager),
    if not await check_admin(user_auth):
        raise Forbidden

    user = await update_object_activate(object_id, db)
    return user


@router.post("/create", response_model=ObjectResponse)
async def create(object_data: ObjectCreate = Body(...), user_id: int = Body(...), user_auth=Depends(manager),
                 files: Optional[List[UploadFile]] = File(...), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    new_object = await create_object(object_data, files, user_id, db)
    return new_object


@router.delete("/delete/{object_id}")
async def delete(object_id: int, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden

    object_delete = await delete_object(object_id, db)
    return object_delete
