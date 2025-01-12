from datetime import datetime

from src.exceptions import ObjectNotFoundException, RoomNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, booking_data: BookingAddRequest, user_id: int):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        hotel = await self.db.hotels.get_one_or_none(id=room.hotel_id)
        current_price = room.price * (booking_data.date_to - booking_data.date_from).days
        _data = BookingAdd(
            user_id=user_id,
            price=current_price,
            created_at=datetime.utcnow(),
            **booking_data.model_dump(),
        )
        try:
            booking = await self.db.bookings.add_booking(booking_data=_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as e:
            raise e

        await self.db.commit()
        return booking
