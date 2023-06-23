# models used by fastapi
import datetime
from typing import List

from pydantic import BaseModel


# TODO use inheritance for all models
class CabinIn(BaseModel):
    user_id: int | None  # keep this field for using this model when testing the db
    name: str
    description: str
    location: str
    latitude: float
    longitude: float
    price: float
    facilities: List[int]
    capacity: int
    nr_beds: int
    nr_rooms: int
    nr_bathrooms: int


class Cabin(CabinIn):
    id: int

    class Config:
        orm_mode = True


class PhotoIn(BaseModel):  # sent to the api
    cabin_id: int
    content: bytes
    principal: bool = False     # also gonna be ignored but not removed yet for backwards compatibility


class Photo(PhotoIn):  # returned from the api
    id: int

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
    booking_id: int
    grade: float
    description: str


class Review(ReviewIn):
    id: int
    user_id: int
    created: datetime.datetime

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    message: str


class UserLogin(BaseModel):
    email: str
    password: str
    role: str = "tourist"


class UserRegister(BaseModel):
    full_name: str
    username: str
    email: str
    role: str = "tourist"
    phone_number: str
    password: str
