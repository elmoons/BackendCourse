from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAddNoPrice

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(db: DBDep, data: BookingAddRequest,  user_id: UserIdDep):
    _data = BookingAddNoPrice(user_id=user_id, **data.model_dump())
    await db.bookings.add(_data)
    await db.commit()
    return {"status": "OK", "data": _data}





