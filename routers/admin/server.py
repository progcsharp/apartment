from typing import List

from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_server
from db.handler.get import get_all_server
from db.handler.update import update_server, server_activate
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.server import ServerResponse, ServerCreate, ServerUpdate
from service.security import manager

router = APIRouter(prefix="/server", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ServerResponse])
async def all(db=Depends(get_db), user_auth=Depends(manager),):
    if not await check_admin(user_auth):
        raise Forbidden
    servers = await get_all_server(db)
    return servers


@router.put("/update", response_model=ServerResponse)
async def update(data_server: ServerUpdate, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden
    server = await update_server(data_server, db)
    return server


@router.put("/activate")
async def activate(server_id: int, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden
    server = await server_activate(server_id, db)
    return server


@router.post("/create", response_model=ServerResponse)
async def create(data_server: ServerCreate, db=Depends(get_db), user_auth=Depends(manager),):
    if not await check_admin(user_auth):
        raise Forbidden
    servers = await create_server(data_server, db)
    return servers
