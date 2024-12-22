import json

import pytest
from src.config import settings
from src.database import engine_null_pool, Base, async_session_maker_null_pool
from src.main import app
from src.models import *
from httpx import AsyncClient, ASGITransport

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_hotels_data_in_database(setup_database):
    with open("tests/mock_hotels.json", "rb") as hotels_file:
        hotels_data_json = hotels_file.read()
        hotels_data = json.loads(hotels_data_json)

    hotels_data_ = [HotelAdd(title=hotel["title"],
                             location=hotel["location"]) for hotel in hotels_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for hotel in hotels_data_:
            await db.hotels.add(hotel)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def add_rooms_data_in_database(add_hotels_data_in_database):
    with open("tests/mock_rooms.json", "rb") as rooms_file:
        rooms_data_json = rooms_file.read()
        rooms_data = json.loads(rooms_data_json)

    rooms_data_ = [RoomAdd(hotel_id=room["hotel_id"],
                           title=room["title"],
                           description=room["description"],
                           price=room["price"],
                           quantity=room["quantity"]) for room in rooms_data]
    print(rooms_data_)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for room in rooms_data_:
            await db.rooms.add(room)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(add_rooms_data_in_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/auth/register", json={
            "email": "kot@pes.com",
            "password": "1234"
        })
