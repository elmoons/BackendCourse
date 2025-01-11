from fastapi_cache.decorator import cache

from datetime import date

from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", description="<h1>Получение отелей<h1>")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Локация"),
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination, title, location, date_from, date_to
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", description="<h1>Добавление отеля<h1>")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 2",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Дубай у фонтана",
                    "location": "ул. Шейха, 4",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "hotel_data": hotel}


@router.delete("/{hotel_id}", description="<h1>Удаление отеля<h1>")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.put("/{hotel_id}", description="<h1>Изменение отеля<h1>")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_data, hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}", description="<h1>Частичное изменение отеля<h1>")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).edit_hotel_partially(hotel_data, hotel_id)
    return {"status": "OK"}
