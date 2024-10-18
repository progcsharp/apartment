from typing import List

from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_tariff
from db.handler.get import get_tariff_by_id, get_all_tariff
from db.handler.update import update_tariff
from schemas.tariff import TariffCreate, TariffResponse, TariffUpdate

router = APIRouter(prefix="/tariff", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[TariffResponse])
async def all(db=Depends(get_db)):
    tariff = await get_all_tariff(db)
    return tariff


@router.get("/id/{id}", response_model=TariffResponse)
async def get(id: int, db=Depends(get_db)):
    tariff = await get_tariff_by_id(id, db)
    return tariff


@router.put("/update", response_model=TariffResponse)
async def update(tariff_data: TariffUpdate, db=Depends(get_db)):
    tariff = await update_tariff(tariff_data, db)
    return tariff


@router.post("/create", response_model=TariffResponse)
async def create(tariff_data: TariffCreate, db=Depends(get_db)):
    tariff = await create_tariff(tariff_data, db)
    return tariff


@router.delete("/delete", response_model=TariffResponse)
async def delete(id: int,  db=Depends(get_db)):
    pass
