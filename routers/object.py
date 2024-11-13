import hashlib
from typing import Optional, List

import boto3
import paginate
from botocore.config import Config
from fastapi import APIRouter, Body, UploadFile, File, Depends

from db.engine import get_db
from db.handler.create import create_object
from db.handler.delete import delete_object
from db.handler.get import get_all_object, get_by_id_object, get_object_by_user_id, get_by_id_object_by_user
from db.handler.update import update_object_activate, update_object_by_id
from schemas.object import ObjectCreate, ObjectResponse, ObjectActivate, ObjectUpdate, ObjectUpdatePhotosConvenience, \
    PublicObject
from service.security import manager

router = APIRouter(prefix="/object", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ObjectResponse])
async def get_all(db=Depends(get_db), user_auth=Depends(manager)):
    objects = await get_all_object(user=user_auth, session=db)
    return objects


@router.get("/id/{object_id}", response_model=PublicObject)
async def get(object_id: int, db=Depends(get_db)):
    objects = await get_by_id_object_by_user(object_id, db)
    return objects


@router.get("/userid/{user_id}", response_model=List[PublicObject])
async def get(user_id: int, offset, limit, db=Depends(get_db)):
    objects = await get_object_by_user_id(user_id, db)
    if objects is None:
        raise
    page = paginate.Page(objects, page=offset, items_per_page=limit)
    return page


@router.put("/activate", response_model=ObjectResponse)
async def activate(object_id: ObjectActivate, user_auth=Depends(manager),
                   db=Depends(get_db)):  # user_auth=Depends(manager),
    user = await update_object_activate(object_id, user_auth, db)
    return user


@router.put("/update", response_model=ObjectResponse)
async def update(convenience_and_removed_photos: ObjectUpdatePhotosConvenience = Body(...), update_object: ObjectUpdate = Body(...),
                 files: Optional[List[UploadFile]] = File(None), db=Depends(get_db), auth_user=Depends(manager)):
    object = await update_object_by_id(update_object, convenience_and_removed_photos, files, db, auth_user)
    return object


@router.post("/create", response_model=ObjectResponse)
async def create(object_data: ObjectCreate = Body(...), files: Optional[List[UploadFile]] = File(...),
                 db=Depends(get_db), user_auth=Depends(manager)):
    new_object = await create_object(object_data, files, user_auth.id, db)
    return new_object


@router.delete("/delete/{object_id}")
async def delete(object_id: int, db=Depends(get_db), user_auth=Depends(manager)):
    object_delete = await delete_object(object_id, user_auth, db)
    return object_delete
