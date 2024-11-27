from fastapi import APIRouter, Body, Depends

from db.engine import get_db
from db.handler.create import create_hashtag
from db.handler.get import get_all_hashtag
from exception.auth import Forbidden
from permission.is_admin import check_admin
from service.security import manager

router = APIRouter(prefix="/hashtag", responses={404: {"description": "Not found"}})


@router.get('/all')
async def get_all(_=Depends(manager), db=Depends(get_db)):
    region = await get_all_hashtag(db)
    return region
