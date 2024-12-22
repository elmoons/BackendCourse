from datetime import datetime, date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    bookings_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2030, month=12, day=12),
        date_to=date(year=2031, month=1, day=1),
        price=100,
        created_at=datetime.utcnow()
    )
    await db.bookings.add(bookings_data)

    booking = await db.bookings.get_one_or_none()
    update_booking = await db.bookings.edit(booking, price=150)
    await db.bookings.delete(id=1)

    await db.commit()
