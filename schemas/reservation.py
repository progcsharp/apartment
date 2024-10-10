from datetime import date

from pydantic import BaseModel


class ReservationBase(BaseModel):
    start_date: date
    end_date: date
    status: str = "new"


class ReservationCreate(ReservationBase):
    object_id: int
    client_id: int
    description: str
