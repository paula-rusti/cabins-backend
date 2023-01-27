from datetime import datetime
from enum import Enum
from typing import List

from sqlmodel import SQLModel


class Facility:
    air_conditioning = 'Air conditioning'
    towels = 'Towels'


class Role(str, Enum):
    owner = 'owner'
    tourist = 'tourist'


class CabinBase(SQLModel):
    name: str
    price: float
    location: str
    description: str
    photos: List[str]
    facilities: List[str]


class UserBase(SQLModel):
    username: str
    full_name: str
    created: datetime
    deleted: bool = False
    role: Role
