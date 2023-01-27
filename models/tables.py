from typing import Optional, List

from sqlmodel import Field, Relationship

from models.models import CabinBase, UserBase


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cabins: Optional[List["Cabin"]] = Relationship(back_populates="user")


class Cabin(CabinBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="cabins")
