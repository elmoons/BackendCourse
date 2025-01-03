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
        created_at=datetime.utcnow(),
    )
    booking = await db.bookings.add(bookings_data)

    new_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    updated_date = date(year=2031, month=1, day=10)
    update_bookings_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2030, month=12, day=12),
        date_to=updated_date,
        price=100,
        created_at=datetime.utcnow(),
    )
    await db.bookings.edit(update_bookings_data, id=booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking.id == booking.id
    assert updated_booking.date_to == updated_date

    booking = await db.bookings.delete(id=new_booking.id)
    assert not booking
