from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Body

from db.engine import get_db
from db.handler.create import create_convenience
from db.handler.delete import delete_convenience
from db.handler.get import get_all_convenience, get_convenience_by_id
from schemas.convenience import ConvenienceResponseList, ConvenienceResponse, ConvenienceCreate, ConvenienceBase

router = APIRouter(prefix="/convenience", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=ConvenienceResponseList)
async def get_all(db=Depends(get_db)):
    convenience = await get_all_convenience(db)
    return {"convenience": convenience}


@router.get("/id/", response_model=ConvenienceResponse)
async def get(id: int, db=Depends(get_db)):
    city = await get_convenience_by_id(id, db)
    return city


@router.post("/create", response_model=ConvenienceResponse)
async def create(convenience_name: ConvenienceCreate, db=Depends(get_db)):
    convenience = await create_convenience(convenience_name, db)
    return convenience


@router.delete("/delete/{convenience_id}")
async def delete(convenience_id: int, db=Depends(get_db)):
    await delete_convenience(convenience_id, db)