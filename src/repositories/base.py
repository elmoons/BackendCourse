import logging

from pydantic import BaseModel
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistException,
)
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as e:
            logging.error(
                f"Не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(e.orig.__cause__)}"
            )
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistException from e
            else:
                logging.error(
                    f"Незнакомая ошибка, не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(e.orig.__cause__)}"
                )
                raise e

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = (
            insert(self.model).values([item.model_dump() for item in data]).returning(self.model)
        )
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        result = await self.session.execute(update_stmt)
        if result.rowcount == 0:
            raise ObjectNotFoundException

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        if result.rowcount == 0:
            raise ObjectNotFoundException
