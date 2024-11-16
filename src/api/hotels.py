from datetime import date

from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", description="<h1>Получение отелей<h1>")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Локация"),
        date_from: date = Query(example="2024-11-01"),
        date_to: date = Query(example="2024-11-10")
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     title=title,
    #     location=location,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", description="<h1>Добавление отеля<h1>")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return hotel


@router.delete("/{hotel_id}", description="<h1>Удаление отеля<h1>")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", description="<h1>Изменение отеля<h1>")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", description="<h1>Частичное изменение отеля<h1>")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
