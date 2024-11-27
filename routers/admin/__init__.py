from fastapi import APIRouter

from routers.admin.apartment import router as apartment
from routers.admin.region import router as region
from routers.admin.city import router as city
from routers.admin.convenience import router as convenience
from routers.admin.object import router as object_router
from routers.admin.user import router as user
from routers.admin.tariff import router as tariff
from routers.admin.client import router as client
from routers.admin.reservation import router as reservation
from routers.admin.server import router as server
from routers.admin.logs import router as logs
from routers.admin.mail import router as mail
from routers.admin.hashtag import router as hashtag

router = APIRouter(prefix="/admin", responses={404: {"description": "Not found"}})

router.include_router(router=apartment)
router.include_router(router=region)
router.include_router(router=reservation)
router.include_router(router=city)
router.include_router(router=convenience)
router.include_router(router=object_router)
router.include_router(router=user)
router.include_router(router=tariff)
router.include_router(router=client)
router.include_router(router=server)
router.include_router(router=logs)
router.include_router(router=mail)
router.include_router(router=hashtag)
