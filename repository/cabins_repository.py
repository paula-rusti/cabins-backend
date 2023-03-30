import datetime
from typing import List, Optional

from pydantic import BaseModel, validator
from sqlalchemy import text, insert
from sqlalchemy.orm import Session

import models.orm_models
from models.dto_models import CabinIn
from models.orm_models import Cabin
from repository.repository import AbstractCabinsRepository


# class CabinFilters(BaseModel):
#     location: Optional[List[str]]
#     price: Optional[dict]  # dict = {min/max: value} or {min: value, max: value}
#
#     @validator("location")
#     def locations_is_valid_array(cls, v):
#         if not all(loc in locations for loc in v):
#             raise ValueError(
#                 "location must be an array of strings representing valid counties"
#             )
#         return v
#
#     @validator("price")
#     def price_range_is_valid(cls, v, values, **kwargs):
#         def valid_number(n):
#             return isinstance(n, int) or isinstance(n, float) and n > 0
#
#         def is_sublist(subset, superset):
#             return all(x in superset for x in subset)
#
#         if v is {}:
#             return v
#         if not (
#             is_sublist(list(v.keys()), ["min", "max"])
#             and all(valid_number(v[key]) for key in v)
#         ):
#             raise ValueError("price object does not respect the required schema")
#         if "min" in v and "max" in v and not v["min"] <= v["max"]:
#             raise ValueError("min price must be less than or equal to max price")
#         return v


class CabinsRepository(AbstractCabinsRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, cabin: CabinIn):
        statement = insert(Cabin).values(
            user_id=cabin.user_id,
            name=cabin.name,
            description=cabin.description,
            location=cabin.location,
            facilities=cabin.facilities,
            price=cabin.price,
            capacity=cabin.capacity,
            nr_beds=cabin.nr_beds,
            nr_rooms=cabin.nr_rooms,
            nr_bathrooms=cabin.nr_bathrooms,
        ).returning(Cabin.id)
        cabin_id = self.db.execute(statement).first()[0]
        self.db.commit()
        return cabin_id

    def get_all(self, skip: int = 0, limit: int = 100):
        # returns all the rows from the table
        return self.db.query(models.orm_models.Cabin).offset(skip).limit(limit).all()

    def get_by_id(self, cabin_id):
        return (
            self.db.query(models.orm_models.Cabin)
            .filter(models.orm_models.Cabin.id == cabin_id)
            .first()
        )

    def get_count(self):
        return self.db.query(models.orm_models.Cabin).count()

    def get_cabins_by_dates(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            location: str = None,
            nr_guests: int = None,
            skip: int = 0,
            limit: int = 0,
    ):
        statement_text = (
            "SELECT * from cabin WHERE id NOT IN (SELECT cabin_id FROM booking WHERE "
            "(start_date  >= :start_date_value AND start_date <= :end_date_value) OR "
            "(end_date  >= :start_date_value AND end_date <= :end_date_value) OR "
            "(start_date  <= :start_date_value AND end_date >= :end_date_value))"
        )
        params_dict = {"start_date_value": start_date, "end_date_value": end_date}
        if location:
            location_query = " AND location LIKE '%' || LOWER(:location_value) || '%'"
            statement_text += location_query
            params_dict["location_value"] = location
        if nr_guests:
            guests_query = " AND capacity >= :nr_guests_value"
            statement_text += guests_query
            params_dict["nr_guests_value"] = nr_guests
        statement_text += " ORDER BY id OFFSET :offset_value LIMIT :limit_value"
        params_dict["offset_value"] = skip
        params_dict["limit_value"] = limit
        statement_text += ";"
        statement = text(statement_text)
        statement = statement.bindparams(**params_dict)
        result = self.db.execute(statement).all()
        return result

    # def get(self, filters: CabinFilters):
    #     # build query based on filters
    #     statement = select(CabinTable)
    #     if filters.location:
    #         statement = statement.where(
    #             or_(*[CabinTable.location == location for location in filters.location])
    #         )
    #     if filters.price:
    #         if "min" in filters.price:
    #             statement = statement.where(CabinTable.price >= filters.price["min"])
    #         if "max" in filters.price:
    #             statement = statement.where(CabinTable.price <= filters.price["max"])
    #     with self.session as session:
    #         results = session.execute(statement.order_by(CabinTable.id))
    #         cabin_list = []
    #         for cabin in results:
    #             cabin_list.append(cabin[0])
    #         return cabin_list
