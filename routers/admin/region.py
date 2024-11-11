from fastapi import Depends, APIRouter

from db.engine import get_db
from db.handler.create import create_region
from db.handler.delete import delete_region
from exception.auth import Forbidden
from permission.is_admin import check_admin
# from routers.admin import router
from schemas.region import RegionCreate, RegionCreateResponse
from service.security import manager

router = APIRouter(prefix="/region", responses={404: {"description": "Not found"}})


@router.post('/create', response_model=RegionCreateResponse)
async def create(region_data: RegionCreate, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    region = await create_region(region_data, db, user_auth)
    return region


@router.delete("/delete/{region_id}")
async def delete(region_id: int, user_auth=Depends(manager), db=Depends(get_db)):

    if not await check_admin(user_auth):
        raise Forbidden

    await delete_region(region_id, db, user_auth.id)

    return "successful"
