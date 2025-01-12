from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    RoomNotFoundException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_all_bookings(db: DBDep):
    bookings = await BookingService(db).get_all_bookings()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await BookingService(db).get_my_bookings(user_id)
    return {"status": "OK", "data": bookings}


@router.post("")
async def add_booking(db: DBDep, booking_data: BookingAddRequest, user_id: UserIdDep):
    try:
        booking = await BookingService(db).add_booking(booking_data, user_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
