from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_region
from db.handler.delete import delete_region
from db.handler.get import get_all_region, get_region_by_id
from schemas.region import RegionResponseList, RegionResponse, RegionCreate, RegionCreateResponse
from service.security import manager

router = APIRouter(prefix="/region", responses={404: {"description": "Not found"}})


@router.get("/all", response_model=RegionResponseList)
async def get_all(db=Depends(get_db), _=Depends(manager)):
    regions = await get_all_region(db)
    return {"regions": regions}


@router.get('/id/{region_id}', response_model=RegionResponse)
async def get_one(region_id: int, db=Depends(get_db), _=Depends(manager)):
    region = await get_region_by_id(region_id, db)
    return region


# @router.post('/create', response_model=RegionCreateResponse)
# async def create(region_data: RegionCreate, db=Depends(get_db)):
#     region = await create_region(region_data, db)
#     return region
#
#
# @router.delete("/delete/{region_id}")
# async def delete(region_id:int, db=Depends(get_db)):
#     await delete_region(region_id, db)
