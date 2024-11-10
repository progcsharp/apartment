from fastapi import Depends, APIRouter

from db.engine import get_db
from db.handler.get import get_logs
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.logs import LogsOut
from service.security import manager

router = APIRouter(prefix="/log", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=LogsOut)
async def get_all(db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise Forbidden

    logs = await get_logs(db)
    return logs
