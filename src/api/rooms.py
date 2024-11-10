from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", description="Получение номеров отеля.")
async def get_hotel_rooms(db: DBDep, hotel_id: int):
    rooms = await db.rooms.get_all(hotel_id=hotel_id)
    return {"status": "OK", "data": rooms}


@router.post("/{hotel_id}/rooms")
async def add_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms/{room_id}", description="Получение конкретного номера отеля.")
async def get_hotel_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.room.get_one_or_none(hotel_id=hotel_id, id=room_id)
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_hotel(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id,  id=room_id)
    await db.commit()
    return {"status": "OK"}
