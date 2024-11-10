from datetime import date

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddNoPrice(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date


class BookingAddWithPrice(BookingAddNoPrice):
    price: int


class Booking(BookingAddWithPrice):
    id: int




