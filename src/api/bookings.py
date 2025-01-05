from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
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
async def add_booking(db: DBDep, booking_data: BookingAddRequest, user_id: UserIdDep):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    current_price = room.price * (booking_data.date_to - booking_data.date_from).days
    _data = BookingAdd(
        user_id=user_id,
        price=current_price,
        created_at=datetime.utcnow(),
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(booking_data=_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()
    return {"status": "OK", "data": booking}
