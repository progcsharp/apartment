from typing import List

from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_reservation
from db.handler.delete import delete_reservation
from db.handler.get import get_reservation_by_object_id, get_reservation_by_user_id, get_reservation_by_id, \
    get_reservation_by_client_id, get_reservation_all_by_admin
from db.handler.update import update_reservation_status, update_reservation
from permission.is_admin import check_admin
from schemas.reservation import ReservationCreate, ReservationResponse, ReservationUpdateStatus, ReservationUpdate
from service.security import manager

router = APIRouter(prefix="/reservation", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=List[ReservationResponse])
async def get_all(user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise
    reservation = await get_reservation_all_by_admin(db)
    return reservation


@router.get("/objectid/{object_id}", response_model=List[ReservationResponse])
async def get_by_object_id(object_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise
    reservation = await get_reservation_by_object_id(user_auth, object_id, db)
    return reservation


#admin
@router.get("/userid/{user_id}", response_model=List[ReservationResponse])
async def get_by_user_id(user_id: int, db=Depends(get_db), user_auth=Depends(manager)):
    if not await check_admin(user_auth):
        raise
    reservation = await get_reservation_by_user_id(user_id, db)
    return reservation


@router.get("/id/{reservation_id}", response_model=ReservationResponse)
async def get_by_id(reservation_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise
    reservation = await get_reservation_by_id(user_auth, reservation_id, db)
    return reservation


@router.get("/clientid/{client_id}", response_model=List[ReservationResponse])
async def get_by_user_id(client_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    if not await check_admin(user_auth):
        raise
    reservation = await get_reservation_by_client_id(user_auth.id, client_id, db)
    return reservation


@router.put("/status")
async def status_update(reservation_status_data: ReservationUpdateStatus, db=Depends(get_db)):
    reservation = await update_reservation_status(reservation_status_data, db)
    return reservation


@router.put("/update", response_model=ReservationResponse)
async def update(reservation_data: ReservationUpdate, user_auth=Depends(manager), db=Depends(get_db)):
    reservation = await update_reservation(user_auth.id, reservation_data, db)
    return reservation


@router.post("/create")
async def create(reservation_data: ReservationCreate, user_auth=Depends(manager), db=Depends(get_db)):
    reservation = await create_reservation(user_auth.id, reservation_data, db)
    return reservation


@router.delete("/delete/{reservation_id}")
async def delete(reservation_id: int, user_auth=Depends(manager), db=Depends(get_db)):
    reservation = await delete_reservation(user_auth.id, reservation_id, db)
    return reservation
