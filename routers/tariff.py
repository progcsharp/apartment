from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi_mail import MessageSchema, MessageType, FastMail

from config import mail_conf
from db.engine import get_db
from db.handler.create import create_tariff
from db.handler.get import get_tariff_by_id, get_all_tariff
from db.handler.update import update_tariff
from schemas.tariff import TariffCreate, TariffResponse, TariffUpdate
from service.security import manager

router = APIRouter(prefix="/tariff", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[TariffResponse])
async def all(db=Depends(get_db), _=Depends(manager)):
    tariff = await get_all_tariff(db)
    return tariff


@router.get("/id/{id}", response_model=TariffResponse)
async def get(id: int, db=Depends(get_db), _=Depends(manager)):
    tariff = await get_tariff_by_id(id, db)
    return tariff


@router.post("id/")
async def activate_tariff(tariff_id: int = Body, db=Depends(get_db), user_auth=Depends(manager)):
    tariff = await get_tariff_by_id(tariff_id, db)
    message = MessageSchema(
        subject="Tariff",
        recipients="fonror@mail.ru",
        body=f"Пользователь с почтой {user_auth.mail} хочет подключить тариф {tariff.name}",
        subtype=MessageType.html)
    fm = FastMail(mail_conf)
    await fm.send_message(message)


# @router.put("/update", response_model=TariffResponse)
# async def update(tariff_data: TariffUpdate, db=Depends(get_db)):
#     tariff = await update_tariff(tariff_data, db)
#     return tariff
#
#
# @router.post("/create", response_model=TariffResponse)
# async def create(tariff_data: TariffCreate, db=Depends(get_db)):
#     tariff = await create_tariff(tariff_data, db)
#     return tariff
#
#
# @router.delete("/delete", response_model=TariffResponse)
# async def delete(id: int,  db=Depends(get_db)):
#     pass
