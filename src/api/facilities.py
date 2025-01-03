from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import AddFacilities
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")

    return await db.facilities.get_all()


@router.post("")
async def add_facilities(db: DBDep, facility: AddFacilities = Body()):
    facility = await db.facilities.add(facility)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}
