# models used by the orm
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY

from db import Base


class Cabin(Base):
    __tablename__ = 'cabin2'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    facilities = Column(ARRAY(Integer))
    price = Column(Float)
