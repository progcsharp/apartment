from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_convenience
from db.handler.delete import delete_convenience
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.convenience import ConvenienceResponse, ConvenienceCreate
from service.security import manager

router = APIRouter(prefix="/convenience", responses={404: {"description": "Not found"}})


@router.post("/create", response_model=ConvenienceResponse)
async def create(convenience_name: ConvenienceCreate, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    convenience = await create_convenience(convenience_name, db, user_auth)
    return convenience


@router.delete("/delete/{convenience_id}")
async def delete(convenience_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    await delete_convenience(convenience_id, db, user_auth.id)
    return "successful"
