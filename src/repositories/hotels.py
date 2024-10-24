from pydantic import BaseModel
from sqlalchemy import func, select, delete, update

from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, title, location, limit, offset):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower().strip()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower().strip()))
        query = (
            query.limit(limit).offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, title, location) -> None:
        query = delete(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower().strip()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower().strip()))
        if location or title:
            await self.session.execute(query)

    async def edit(self, update_data: Hotel, title, location) -> None:
        query = update(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower().strip()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower().strip()))
        if location or title:
            query = query.values(title=update_data.title, location=update_data.location)
            await self.session.execute(query)
