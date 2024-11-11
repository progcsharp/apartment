from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_apartment
from db.handler.delete import delete_apartment
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.apartment import ApartmentResponse, ApartmentCreate
from service.security import manager

router = APIRouter(prefix="/property-type", responses={404: {"description": "Not found"}})


@router.post("/create", response_model=ApartmentResponse)
async def create(apartment_data: ApartmentCreate, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    apartment = await create_apartment(apartment_data, db, user_auth)
    return apartment


@router.delete("/delete/{apartment_id}")
async def delete(apartment_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    await delete_apartment(apartment_id, db, user_auth.id)
    return "successful"
