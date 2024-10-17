from sqlalchemy import select

from src.database import async_session_maker


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
