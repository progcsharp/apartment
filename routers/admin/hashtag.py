from fastapi import APIRouter, Body, Depends

from db.engine import get_db
from db.handler.create import create_hashtag
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.hashtag import Hashtag
from service.security import manager

router = APIRouter(prefix="/hashtag", responses={404: {"description": "Not found"}})


@router.post('/create')
async def create(name: Hashtag = Body(...), user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    region = await create_hashtag(name, db, user_auth)
    return region


# @router.delete("/delete/{region_id}")
# async def delete(region_id: int, user_auth=Depends(manager), db=Depends(get_db)):
#
#     if not await check_admin(user_auth):
#         raise Forbidden
#
#     await delete_region(region_id, db, user_auth.id)
#
#     return "successful"
