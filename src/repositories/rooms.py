from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]

    async def get_one_or_none_room_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(joinedload(self.model.facilities))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]
