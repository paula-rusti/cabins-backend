# models used by fastapi
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


class PhotoCreate(BaseModel):   # sent from the api
    cabin_id: int
    content: bytes
    principal: bool = False


class Photo(BaseModel):     # returned from the api
    id: int
    cabin_id: int
    content: bytes
    principal: bool = False
