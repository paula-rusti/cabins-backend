from sqlalchemy import text
from sqlalchemy.orm import Session

from repository.repository import AbstractReviewRepository
from models import dto_models, orm_models


class ReviewRepository(AbstractReviewRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, review, user_id):
        # validate that the specified booking exist and only then add to db
        pass

    def get_reviews_of_cabin(self, cabin_id, skip, limit):
        return (
            self.db.query(orm_models.Review)
            .filter(orm_models.Review.cabin_id == int(cabin_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_reviews_of_tourist(self, user_id, skip, limit):
        return (
            self.db.query(orm_models.Review)
            .filter(orm_models.Review.user_id == int(user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_review_of_booking(self, user_id):
        pass

    def get_review(self, _id):
        pass
