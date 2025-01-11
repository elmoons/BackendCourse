from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import AddFacilities
from src.services.facilities import FacilityService
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def add_facilities(db: DBDep, facility: AddFacilities = Body()):
    facility = await FacilityService(db).create_facility(facility)
    return {"status": "OK", "data": facility}
