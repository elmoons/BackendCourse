from datetime import date

from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Query

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, CheckInDateLaterOutDate
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", description="Получение номеров отеля.")
async def get_hotel_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-10"),
):
    try:
        rooms = await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return {"status": "OK", "data": rooms}
    except CheckInDateLaterOutDate as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отель не найден")
    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms/{room_id}", description="Получение конкретного номера отеля.")
async def get_hotel_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one_room_with_rels(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_hotel(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.edit(_room_data, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    try:
        await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}
