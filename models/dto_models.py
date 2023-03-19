# models used by fastapi
import datetime
from typing import List

from pydantic import BaseModel


# use inheritance
class CabinCreate(BaseModel):
    user_id: int
    name: str
    description: str
    location: str
    price: float
    facilities: List[int]
    capacity: int
    nr_beds: int
    nr_rooms: int
    nr_bathrooms: int


class Cabin(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    location: str
    price: float
    facilities: List[int]
    capacity: int
    nr_beds: int
    nr_rooms: int
    nr_bathrooms: int

    class Config:
        orm_mode = True


class PhotoCreate(BaseModel):  # sent from the api
    cabin_id: int
    content: bytes
    principal: bool = False


class Photo(BaseModel):  # returned from the api
    id: int
    cabin_id: int
    content: bytes
    principal: bool = False

    class Config:
        orm_mode = True


class BookingCreate(BaseModel):
    cabin_id: int
    user_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    price: float
    nr_guests: int


class Booking(BookingCreate):
    id: int

    class Config:
        orm_mode = True


class ReviewIn(BaseModel):
    cabin_id: int
    grade: float
    description: str


class Review(ReviewIn):
    id: int
    user_id: int
    created: datetime.datetime

    class Config:
        orm_mode = True
