from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import AddFacilities

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    facilities = await db.facilities.get_all()
    return {"status": "OK", "data": facilities}


@router.post("")
async def add_facilities(db: DBDep, facility: AddFacilities = Body()):
    facility = await db.facilities.add(facility)
    await db.commit()
    return {"status": "OK", "data": facility}
