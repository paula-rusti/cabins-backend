from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Role(str, Enum):
    owner = 'owner'
    tourist = 'tourist'


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: str
    created: datetime
    deleted: bool = False
    role: Role
    cabins: Optional[List["Cabin"]] = Relationship(back_populates="user")


class Facility:
    air_conditioning = 'Air conditioning'
    towels = 'Towels'


class Cabin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    price: float
    location: str
    description: str
    photos: List[str]
    facilities: List[str]
    user: "User" = Relationship(back_populates="cabins")
