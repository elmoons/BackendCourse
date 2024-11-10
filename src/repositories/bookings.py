from sqlalchemy import insert, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking, BookingAddNoPrice, BookingAddWithPrice
from src.schemas.rooms import Room


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def add(self, data: BookingAddNoPrice):
        query = select(RoomsOrm).filter_by(id=data.room_id)
        result = await self.session.execute(query)
        a = result.scalars().one_or_none()
        room = Room.model_validate(a, from_attributes=True)
        price = room.price * (data.date_to - data.date_from).days
        _data = BookingAddWithPrice(price=price, **data.model_dump())

        add_data_stmt = insert(self.model).values(**_data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)
