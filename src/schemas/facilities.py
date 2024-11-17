from pydantic import BaseModel


class Facilities(BaseModel):
    id: int
    title: str


class AddFacilities(BaseModel):
    title: str
