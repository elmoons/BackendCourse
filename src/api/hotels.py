from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from sqlalchemy import insert, select, func
from src.models. hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", description="<h1>Получение отелей<h1>")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Локация"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("", description="<h1>Добавление отеля<h1>")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул. Моря, 2",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Дубай у фонтана",
        "location": "ул. Шейха, 4",
    }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", description="<h1>Удаление отеля<h1>")
async def delete_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(
            title=hotel_data.title,
            location=hotel_data.location
        )
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", description="<h1>Изменение отеля<h1>")
async def put_hotel(hotel_data: Hotel, update_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            update_data,
            title=hotel_data.title,
            location=hotel_data.location,
        )
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", description="<h1>Частичное изменение отеля<h1>")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}
