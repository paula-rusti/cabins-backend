from typing import Optional, List

from sqlalchemy import LargeBinary, Column
from sqlmodel import Field, Relationship, SQLModel

from models.models import CabinBase, UserBase


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cabins: Optional[List["Cabin"]] = Relationship(back_populates="user")


class Cabin(CabinBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="cabins")


class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cabin_id: Optional[int] = Field(default=None, foreign_key="cabin.id")
    content: bytes = Field(default=None, sa_column=Column(LargeBinary))
    principal: bool = False
