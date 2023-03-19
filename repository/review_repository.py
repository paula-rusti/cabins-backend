from sqlalchemy import text
from sqlalchemy.orm import Session

from repository.repository import AbstractReviewRepository
from models import dto_models, orm_models


class ReviewRepository(AbstractReviewRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_review(self, review: dto_models.ReviewIn, user_id: int):
        statement_text = """
            INSERT INTO review (
              user_id,
              cabin_id,
              grade,
              description
            )
            SELECT * FROM (VALUES (2, 9, 10, 'from console'))
                     AS t (r_user_id, r_cabin_id, r_grade, r_description)
            WHERE (
                SELECT EXISTS(SELECT "user".id FROM "user"
                    WHERE role = 'tourist'
                      AND EXISTS(SELECT * from booking WHERE booking.end_date < now()::date 
                                                         AND booking.user_id = t.r_user_id 
                                                         AND booking.cabin_id = t.r_cabin_id)
                      AND NOT EXISTS(SELECT * from review WHERE cabin_id = t.r_cabin_id))
            ) RETURNING id;
        """
        params = {
            "user_id": user_id,
            "cabin_id": review.cabin_id,
            "grade": review.grade,
            "description": review.description,
        }
        statement = text(statement_text).bindparams(**params)
        result = self.db.execute(statement)
        self.db.commit()
        ff = result.first()
        return ff

    def get_reviews_of_cabin(self, cabin_id, skip, limit):
        return (
            self.db.query(orm_models.Review)
            .filter(orm_models.Review.cabin_id == int(cabin_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_reviews_by_tourist(self, user_id, skip, limit):
        return (
            self.db.query(orm_models.Review)
            .filter(orm_models.Review.user_id == int(user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
