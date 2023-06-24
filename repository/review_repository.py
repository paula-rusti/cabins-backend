from sqlalchemy import insert
from sqlalchemy.orm import Session

import models
from models import orm_models
from models.dto_models import ReviewIn
from models.orm_models import Review
from repository.repository import AbstractReviewRepository


class ReviewRepository(AbstractReviewRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, review: ReviewIn, user_id):
        existing_review = self.db.query(orm_models.Review).filter(
            orm_models.Review.user_id == user_id,
            orm_models.Review.cabin_id == review.cabin_id,
            orm_models.Review.booking_id == review.booking_id,
        ).first()
        if existing_review:
            return None

        statement = (
            insert(Review)
            .values(
                user_id=user_id,
                cabin_id=review.cabin_id,
                booking_id=review.booking_id,
                grade=review.grade,
                description=review.description
            )
            .returning(Review.id)
        )
        review_id = self.db.execute(statement).first()[0]
        self.db.commit()
        return review_id

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
        # TODO implement and use this instead of session in review router
        pass

    def get_review(self, _id):
        return (
            self.db.query(models.orm_models.Review)
            .filter(models.orm_models.Review.id == _id)
            .first()
        )
