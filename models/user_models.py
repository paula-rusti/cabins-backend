from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class Role(str, Enum):
    owner = 'owner'
    tourist = 'tourist'


class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: str
    created: datetime
    deleted: bool = False
    role: Role



