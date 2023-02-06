from datetime import datetime
from enum import Enum
from typing import List

import sqlalchemy
from sqlalchemy import ARRAY, String, Column
from sqlmodel import SQLModel, Field


class Facility:
    air_conditioning = "Air conditioning"
    towels = "Towels"


class Role(str, Enum):
    owner = "owner"
    tourist = "tourist"


class CabinBase(SQLModel):
    name: str
    price: float
    location: str
    description: str
    facilities: List[str] = Field(default=None, sa_column=Column(ARRAY(String())))


class UserBase(SQLModel):
    username: str
    full_name: str
    created: datetime
    deleted: bool = False
    role: Role = Field(sa_column=Column(sqlalchemy.types.Enum(Role)))