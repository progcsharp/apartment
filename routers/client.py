from typing import List

from fastapi import APIRouter, Body, Depends

from db.engine import get_db
from db.handler.create import create_client
from db.handler.delete import client_delete
from db.handler.get import get_all_client, get_client_by_phone, get_client_by_id
from schemas.client import ClientCreate, ClientResponse, ClientResponseList
from service.security import manager

router = APIRouter(prefix="/client", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ClientResponseList])
async def all(db=Depends(get_db), user_auth=Depends(manager)):
    client = await get_all_client(session=db, user=user_auth)
    return client

# #admin
# @router.get("/userid/{user_id}", response_model=ClientResponse)
# async def get_by_user_id(user_id: int, db=Depends(get_db)):
#     client = await get_client_by_id(user_id, db)
#     return client


@router.get("/phone/{phone}", response_model=ClientResponse)
async def get_by_user_id(phone: str, db=Depends(get_db), _=Depends(manager)):
    client = await get_client_by_phone(phone, db)
    return client


@router.get("/id/{client_id}", response_model=ClientResponse)
async def get_by_id(client_id: int, db=Depends(get_db), _=Depends(manager)):
    client = await get_client_by_id(client_id, db)
    return client


@router.post("/create", response_model=ClientResponse)
async def create(client_data: ClientCreate, user_auth=Depends(manager), db=Depends(get_db)):
    client = await create_client(client_data=client_data, user_id=user_auth.id, session=db)
    return client


@router.delete("/delete/{client_id}")
async def delete(client_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    client = await client_delete(user=user_auth, client_id=client_id, session=db)
    return client
