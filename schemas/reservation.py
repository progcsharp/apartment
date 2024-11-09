from datetime import date

from pydantic import BaseModel


class Client(BaseModel):
    id: int
    fullname: str
    phone: str
    email: str


class Object(BaseModel):
    id: int
    name: str


class ReservationBase(BaseModel):
    start_date: date
    end_date: date


class ReservationCreate(ReservationBase):
    object_id: int
    client_id: int
    description: str
    status: str = "new"
    letter: str
    guest_count: int


class ReservationResponse(ReservationBase):
    id: int
    status: str
    description: str
    client: Client
    object: Object
    letter: str
    guest_count: int


class ReservationUpdateStatus(BaseModel):
    id: int
    status: str


class ReservationUpdate(BaseModel):
    id: int
    object_id: int
    start_date: date
    end_date: date
    description: str
    status: str
    letter: str
    guest_count: int


class ClientData(BaseModel):
    fullname: str
    phone: str
    email: str


class ReservationData(ReservationBase):
    object_id: int
    description: str
    guest_count: int