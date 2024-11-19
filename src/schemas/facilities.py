from pydantic import BaseModel


class AddFacilities(BaseModel):
    title: str


class Facilities(AddFacilities):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
