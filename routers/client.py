from typing import List

from fastapi import APIRouter, Body, Depends

from db.engine import get_db
from db.handler.create import create_client
from db.handler.get import get_all_client, get_client_by_id
from schemas.client import ClientCreate, ClientResponse

router = APIRouter(prefix="/client", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ClientResponse])
async def all(db=Depends(get_db)):
    client = await get_all_client(db)
    return client


@router.get("/userid", response_model=ClientResponse)
async def get_by_user_id(user_id: int, db=Depends(get_db)):
    client = await get_client_by_id(user_id, db)
    return client


@router.post("/create", response_model=ClientResponse)
async def create(client_data: ClientCreate, user_id: int = Body(...), db=Depends(get_db)):
    client = await create_client(client_data, user_id, db)
    return client


@router.delete("/delete")
async def delete(id: int, db=Depends(get_db)):
    pass
