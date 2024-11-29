from fastapi import APIRouter, Body, Depends

from db.engine import get_db
from db.handler.create import create_hashtag
from db.handler.delete import delete_hashtag
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.hashtag import Hashtag
from service.security import manager

router = APIRouter(prefix="/hashtag", responses={404: {"description": "Not found"}})


@router.post('/create')
async def create(name: Hashtag = Body(...), user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    region = await create_hashtag(name.name, db, user_auth)
    return region


@router.delete("/delete/{hashtag_id}")
async def delete(hashtag_id: int, user_auth=Depends(manager), db=Depends(get_db)):

    if not await check_admin(user_auth):
        raise Forbidden

    await delete_hashtag(hashtag_id, db, user_auth.id)

    return "successful"
