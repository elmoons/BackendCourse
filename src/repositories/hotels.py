from sqlalchemy import func, select

from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


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
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()