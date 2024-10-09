from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    name: str | None = Field(default=None)
