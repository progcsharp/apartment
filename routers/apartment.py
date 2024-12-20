from typing import List

from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_apartment
from db.handler.delete import delete_apartment
from db.handler.get import get_all_apartment, get_apartment_by_id
from schemas.apartment import ApartmentResponseList, ApartmentResponse, ApartmentCreate
from service.security import manager

router = APIRouter(prefix="/property-type", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ApartmentResponseList])
async def get_all(db=Depends(get_db), _=Depends(manager)):
    apartments = await get_all_apartment(db)
    return apartments


@router.get("/id/{apartment_id}", response_model=ApartmentResponse)
async def get(apartment_id: int, db=Depends(get_db), _=Depends(manager)):
    apartment = await get_apartment_by_id(apartment_id, db)
    return apartment


# @router.post("/create", response_model=ApartmentResponse)
# async def create(apartment_data: ApartmentCreate, db=Depends(get_db)):
#     apartment = await create_apartment(apartment_data, db)
#     return apartment
#
#
# @router.delete("/delete/{apartment_id}")
# async def delete(apartment_id: int, db=Depends(get_db)):
#     await delete_apartment(apartment_id, db)
#     return "successful"
#
