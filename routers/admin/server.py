from typing import List

from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_server
from db.handler.get import get_all_server
from schemas.server import ServerResponse, ServerCreate
from service.security import manager

router = APIRouter(prefix="/server", responses={404: {"description": "Not found"}})


@router.post("/create", response_model=ServerResponse)
async def create(data_server: ServerCreate, db=Depends(get_db)):
    servers = await create_server(data_server, db)
    return servers
