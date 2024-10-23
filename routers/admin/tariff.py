from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_tariff
from db.handler.update import update_tariff
from exception.auth import Forbidden
from permission.is_admin import check_admin
from schemas.tariff import TariffResponse, TariffUpdate, TariffCreate
from service.security import manager

router = APIRouter(prefix="/tariff", responses={404: {"description": "Not found"}})


@router.put("/update", response_model=TariffResponse)
async def update(tariff_data: TariffUpdate, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    tariff = await update_tariff(tariff_data, db)
    return tariff


@router.post("/create", response_model=TariffResponse)
async def create(tariff_data: TariffCreate, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise Forbidden

    tariff = await create_tariff(tariff_data, db)
    return tariff
