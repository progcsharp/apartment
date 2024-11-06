from typing import List

from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.get import get_all_server
from schemas.server import ServerResponse
from service.security import manager

router = APIRouter(prefix="/server", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ServerResponse])
async def all(db=Depends(get_db)):
    servers = await get_all_server(db)
    return servers
