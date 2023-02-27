from typing import List, Optional

from pydantic import BaseModel, validator
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlmodel import select

import models.orm_models
from models.dto_models import CabinCreate
from models.orm_models import Cabin
from models.tables import CabinTable
from repository.repository import AbstractCabinsRepository
from scripts.data import locations


class CabinFilters(BaseModel):
    location: Optional[List[str]]
    price: Optional[dict]  # dict = {min/max: value} or {min: value, max: value}

    @validator("location")
    def locations_is_valid_array(cls, v):
        if not all(loc in locations for loc in v):
            raise ValueError(
                "location must be an array of strings representing valid counties"
            )
        return v

    @validator("price")
    def price_range_is_valid(cls, v, values, **kwargs):
        def valid_number(n):
            return isinstance(n, int) or isinstance(n, float) and n > 0

        def is_sublist(subset, superset):
            return all(x in superset for x in subset)

        if v is {}:
            return v
        if not (
            is_sublist(list(v.keys()), ["min", "max"])
            and all(valid_number(v[key]) for key in v)
        ):
            raise ValueError("price object does not respect the required schema")
        if "min" in v and "max" in v and not v["min"] <= v["max"]:
            raise ValueError("min price must be less than or equal to max price")
        return v


class CabinsRepository(AbstractCabinsRepository):
    def __init__(self, session, db: Session):
        self.session = session
        self.db = db

    def add(self, cabin: CabinCreate):
        self.db.add(Cabin(**cabin.dict()))
        self.db.commit()

    def get(self, filters: CabinFilters):
        # build query based on filters
        statement = select(CabinTable)
        if filters.location:
            statement = statement.where(
                or_(*[CabinTable.location == location for location in filters.location])
            )
        if filters.price:
            if "min" in filters.price:
                statement = statement.where(CabinTable.price >= filters.price["min"])
            if "max" in filters.price:
                statement = statement.where(CabinTable.price <= filters.price["max"])
        with self.session as session:
            results = session.execute(statement.order_by(CabinTable.id))
            cabin_list = []
            for cabin in results:
                cabin_list.append(cabin[0])
            return cabin_list

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.orm_models.Cabin).offset(skip).limit(limit).all()

        # statement = select(CabinTable)  # select * from cabins
        # with self.session as session:
        #     cabins = session.execute(statement)
        #     cabins_list = []
        #     for c in cabins:
        #         cabins_list.append(c[0])
        #     return cabins_list

    def get_count(self):
        return self.db.query(models.orm_models.Cabin).count()

    def get_cabin_by_id(self, cabin_id):
        statement = select(CabinTable).where(CabinTable.id == cabin_id)
        with self.session as session:
            cabin = session.execute(statement).first()
            return cabin
