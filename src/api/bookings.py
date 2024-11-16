from datetime import datetime

from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}


@router.post("")
async def add_booking(db: DBDep, booking_data: BookingAddRequest,  user_id: UserIdDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    current_price = room.price * (booking_data.date_to - booking_data.date_from).days
    _data = BookingAdd(user_id=user_id, price=current_price, created_at=datetime.utcnow(), **booking_data.model_dump())
    booking = await db.bookings.add(_data)
    await db.commit()
    return {"status": "OK", "data": booking}

