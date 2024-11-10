from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_city
from db.handler.delete import delete_city
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.city import CityResponse, CityCreate
from service.security import manager

router = APIRouter(prefix="/city", responses={404: {"description": "Not found"}})


@router.post("/create", response_model=CityResponse)
async def create(city_data: CityCreate, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    city = await create_city(city_data, db, user_auth)
    return city


@router.delete("/delete/{city_id}")
async def delete(city_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    await delete_city(city_id, db)
    return "successful"
