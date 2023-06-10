import datetime
from typing import List

from sqlalchemy import text, insert
from sqlalchemy.orm import Session

import models.orm_models
from models.dto_models import CabinIn
from models.orm_models import Cabin
from repository.repository import AbstractCabinsRepository


class CabinsRepository(AbstractCabinsRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, cabin: CabinIn, user_id: int):
        statement = (
            insert(Cabin)
            .values(
                user_id=user_id,  # taken from the header
                name=cabin.name,
                description=cabin.description,
                location=cabin.location,
                latitude=cabin.latitude,
                longitude=cabin.longitude,
                facilities=cabin.facilities,
                price=cabin.price,
                capacity=cabin.capacity,
                nr_beds=cabin.nr_beds,
                nr_rooms=cabin.nr_rooms,
                nr_bathrooms=cabin.nr_bathrooms,
            )
            .returning(Cabin.id)
        )
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

    def _is_sublist(self, lst1, lst2):
        return set(lst2) <= set(lst1)

    def get_filtered_cabins(
        self,
        user_id: int,
        location: str | None,
        capacity: int | None,
        rating: int | None,
        start_date: datetime.date | None,
        end_date: datetime.date | None,
        min_price: int | None,
        max_price: int | None,
        has_facility: List[str] | None,
        skip: int,
        limit: int,
    ):
        """
        varianta tiganeasca care le ia pe toate din db si face filtrarea la nivel de python, nu din sql query
        """
        all_cabins = self.db.query(models.orm_models.Cabin).all()
        filtered = all_cabins

        if user_id:
            filtered = list(filter(lambda cabin: cabin.user_id == user_id, filtered))

        if location is not None:
            filtered = list(filter(lambda cabin: cabin.location == location, filtered))
        if capacity is not None:
            filtered = list(filter(lambda cabin: cabin.capacity >= capacity, filtered))
        if min_price:
            filtered = list(filter(lambda cabin: cabin.price >= min_price, filtered))
        if max_price:
            filtered = list(filter(lambda cabin: cabin.price <= max_price, filtered))

        # now filter by included facilities
        if has_facility is not None:
            filtered_by_included_facilities = []
            for cabin in filtered:
                current_facilities = [
                    list(facility.split("_"))[0] for facility in cabin.facilities
                ]  # list = ['spa', 'spa/description', 'wifi', 'wifi/desc']
                if self._is_sublist(current_facilities, has_facility):
                    filtered_by_included_facilities.append(cabin)
            filtered = filtered_by_included_facilities

        # now make another query to retrieve all reviews of all cabins and compute their rating
        if rating is not None:
            filtered_by_rating = []
            reviews = self.db.query(models.orm_models.Review).all()
            for cabin in filtered:
                reviews_of_cabin = list(
                    filter(lambda review: review.cabin_id == cabin.id, reviews)
                )
                if len(reviews_of_cabin) == 0:
                    continue
                grades_sum = sum([review.grade for review in reviews_of_cabin])
                computed_rating = grades_sum / (len(reviews_of_cabin))
                if computed_rating >= rating:
                    filtered_by_rating.append(cabin)
            filtered = filtered_by_rating

        # now get only the cabins which are free in the specified period
        if start_date and end_date:
            params_dict = {"start_date_value": start_date, "end_date_value": end_date}
            statement_text = (
                "SELECT id from cabin WHERE id NOT IN (SELECT cabin_id FROM booking WHERE "
                "(start_date  >= :start_date_value AND start_date <= :end_date_value) OR "
                "(end_date  >= :start_date_value AND end_date <= :end_date_value) OR "
                "(start_date  <= :start_date_value AND end_date >= :end_date_value))"
            )
            statement = text(statement_text)
            statement = statement.bindparams(**params_dict)
            free_cabins = [row[0] for row in self.db.execute(statement).all()]
            free_and_filtered_cabins = [
                cabin for cabin in filtered if cabin in free_cabins
            ]
            filtered = free_and_filtered_cabins

        return filtered[skip : skip + limit]
