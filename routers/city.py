from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_city
from db.handler.delete import delete_city
from db.handler.get import get_all_cities, get_city_by_id
from schemas.city import CityResponseList, CityResponse, CityCreate

router = APIRouter(prefix="/city", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=CityResponseList)
async def get_all(db=Depends(get_db)):
    cities = await get_all_cities(db)
    return {"cities":cities}


@router.get("/id/", response_model=CityResponse)
async def get(id,db=Depends(get_db)):
    city = await get_city_by_id(int(id), db)
    return city


@router.post("/create", response_model=CityResponse)
async def create(city_data: CityCreate, db=Depends(get_db)):
    city = await create_city(city_data, db)
    return city


@router.delete("/delete")
async def delete(id:int, db=Depends(get_db)):
    await delete_city(id, db)
    return "successful"




