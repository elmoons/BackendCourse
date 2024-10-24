from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker, engine


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

    async def add(self, data: BaseModel):
        add_data_stat = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stat)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        query = update(self.model)
        await self.session.execute(query)

    async def delete(self, **filter_by) -> None:
        query = delete(self.model)
        await self.session.execute(query)
