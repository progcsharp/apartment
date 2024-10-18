from typing import Optional, List

from fastapi import APIRouter, Body, UploadFile, File, Depends

from db.engine import get_db
from db.handler.create import create_object
from db.handler.delete import delete_object
from db.handler.get import get_all_object, get_by_id_object, get_object_by_user_id
from db.handler.update import update_object_activate
from schemas.object import ObjectCreate, ObjectResponse, ObjectActivate
from service.security import manager

router = APIRouter(prefix="/object", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ObjectResponse])
async def get_all(db=Depends(get_db)):
    objects = await get_all_object(db)
    return objects


@router.get("/id/{id}", response_model=ObjectResponse)
async def get(id: int, db=Depends(get_db)):
    objects = await get_by_id_object(id, db)
    if objects is None:
        raise
    return objects


@router.get("/userid/{user_id}", response_model=List[ObjectResponse])
async def get(user_id: int, db=Depends(get_db)):
    objects = await get_object_by_user_id(user_id, db)
    if objects is None:
        raise
    return objects


@router.put("/activate", response_model=ObjectResponse)
async def activate(object_id: ObjectActivate,   db=Depends(get_db)):#user_auth=Depends(manager),
    user = await update_object_activate(object_id, db)
    return user


@router.post("/create", response_model=ObjectResponse)
async def create(object_data: ObjectCreate = Body(...), files: Optional[List[UploadFile]] = File(...), db=Depends(get_db)):
    new_object = await create_object(object_data, files, 3, db)
    return new_object


@router.delete("/delete")
async def delete(id: int, db=Depends(get_db)):
    object_delete = await delete_object(id, db)
    return object_delete
