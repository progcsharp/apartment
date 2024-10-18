from fastapi import APIRouter, Depends

from db.engine import get_db
from db.handler.create import create_region
from db.handler.delete import delete_region
from db.handler.get import get_all_region, get_region_by_id
from schemas.region import RegionResponseList, RegionResponse, RegionCreate, RegionCreateResponse

router = APIRouter(prefix="/region", responses={404: {"description": "Not found"}})


# @router.get("/test")
# async def get_all(db=Depends(get_db)):
#     regions = await count_objects_in_region(db)
#     print(regions)
#     for region in regions:
#         print(region[0].name, region[1])
#     return "regions"


@router.get("/all/", response_model=RegionResponseList)
async def get_all(db=Depends(get_db)):
    regions = await get_all_region(db)
    return {"regions": regions}


@router.get('/id/', response_model=RegionResponse)
async def get_one(id: int, db=Depends(get_db)):
    region = await get_region_by_id(id, db)
    return region


@router.post('/create', response_model=RegionCreateResponse)
async def create(region_data: RegionCreate, db=Depends(get_db)):
    region = await create_region(region_data, db)
    return region


@router.delete("/delete")
async def delete(id:int, db=Depends(get_db)):
    await delete_region(id, db)
    return "successful"
