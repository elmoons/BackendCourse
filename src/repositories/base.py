from sqlalchemy import select, insert

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

    async def add(self, data: model):
        add_hotel_stat = insert(self.model).values(**data.model_dump())
        print(add_hotel_stat.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_hotel_stat)
        return data

