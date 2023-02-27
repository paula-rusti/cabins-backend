# models used by fastapi
from typing import List

from pydantic import BaseModel


class CabinCreate(BaseModel):
    name: str
    description: str
    location: str
    price: float
    facilities: List[int]


class Cabin(BaseModel):
    id: int
    name: str
    description: str
    location: str
    price: float
    facilities: List[int]

    class Config:
        orm_mode = True
