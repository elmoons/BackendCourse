from datetime import date
from http.client import HTTPException

from sqlalchemy import insert, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data, free_rooms):
        bookings_query = (
            select(BookingsOrm)
            .filter(BookingsOrm.room_id == booking_data.room_id)
        )
        result = await self.session.execute(bookings_query)
        bookings = result.scalars().all()
        bookings_count = len(bookings)

        quantity_room = len(free_rooms)

        if bookings_count < quantity_room:
            booking = await BaseRepository.add(self, data=booking_data)
            return self.mapper.map_to_domain_entity(booking)
        else:
            return "На данные даты эти комнаты уже забронированы."
