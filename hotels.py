from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@router.get("", description="<h1>Получение отелей<h1>")
def get_hotels(
        title: str | None = Query(default=None, description="Название отеля"),
        id: int | None = Query(default=None, description="Айдишник")
):
    hotels_ = []
    for hotel in hotels:
        if id and id != hotel["id"]:
            continue
        if title and title != hotel["title"]:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("", description="<h1>Добавление отеля<h1>")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@router.delete("/{hotel_id}", description="<h1>Удаление отеля<h1>")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.put("/{hotel_id}", description="<h1>Изменение отеля<h1>")
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}


@router.patch("/{hotel_id}", description="<h1>Частичное изменение отеля<h1>")
def patch_hotel(hotel_id: int, title: str | None = Body(default=None), name: str | None = Body(default=None)):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}
