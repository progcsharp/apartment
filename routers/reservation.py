from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_reservation
from db.handler.get import get_reservation_by_object_id, get_reservation_by_user_id
from schemas.reservation import ReservationCreate

router = APIRouter(prefix="/reservation", responses={404: {"description": "Not found"}})


@router.get("/objectid")
async def get_by_object_id(object_id: int, db=Depends(get_db)):
    reservation = await get_reservation_by_object_id(object_id, db)
    return reservation


@router.get("/userid")
async def get_by_user_id(user_id: int, db=Depends(get_db)):
    reservation = await get_reservation_by_user_id(user_id, db)
    return reservation


@router.post("/create")
async def create(reservation_data: ReservationCreate, db=Depends(get_db)):
    reservation = await create_reservation(reservation_data, db)
    return reservation
