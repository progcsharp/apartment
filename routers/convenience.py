from fastapi import APIRouter, Depends, UploadFile, File

from db.engine import get_db
from db.handler.delete import delete_convenience
from db.handler.get import get_all_convenience, get_convenience_by_id
from schemas.convenience import ConvenienceResponseList, ConvenienceResponse, ConvenienceCreate

router = APIRouter(prefix="/convenience", responses={404: {"description": "Not found"}})


@router.get("/all")
async def get_all(db=Depends(get_db)):
    convenience = await get_all_convenience(db)
    return {"convenience": convenience}


@router.get("/id/", response_model=ConvenienceResponse)
async def get(id, db=Depends(get_db)):
    city = await get_convenience_by_id(id, db)
    return city


@router.post("/create", response_model=ConvenienceResponse)
async def create(convenience_data: ConvenienceCreate, file: UploadFile=File(...), db=Depends(get_db)):
    pass


@router.delete("/delete")
async def delete(id:int, db=Depends(get_db)):
    await delete_convenience(id, db)
    return "successful"



