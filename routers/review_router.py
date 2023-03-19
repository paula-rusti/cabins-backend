import dataclasses

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from db import get_db
from models import orm_models, dto_models
from repository.review_repository import ReviewRepository
from utils.auth_user import User, authorize_user

router = APIRouter(prefix="/reviews", tags=["reviews"])


def pagination_params(page: int = 1, size: int = 10):
    return (page - 1) * size, size


def review_repository(db=Depends(get_db)):
    return ReviewRepository(db=db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_review(
        review: dto_models.ReviewIn,
        user: User = Depends(authorize_user),
        repo: ReviewRepository = Depends(review_repository),
):
    """The review can be inserted if the user booked that cabin in the past
    and the user did not review that cabin previously
    This route will be authenticated and the user id is extracted from a header for mocking demo"""
    inserted = repo.add_review(review=review, user_id=user.user_id)
    if not inserted:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Review cannot be added")
    return {"detail": "Review added"}


@router.get("/")
def get_reviews(
        cabin_id: int = None,
        user_id: int = None,
        pagination=Depends(pagination_params),
        db: Session = Depends(get_db),
):
    """Provide either cabin_id or user_id to retrieve either the reviews of a cabin or the reviews provided by a user"""
    if not cabin_id and not user_id:
        raise HTTPException(
            status_code=500,
            detail="Bad Request",
            headers={
                "X-Error": "At least one query param (cabin_id, user_id) must be specified"
            },
        )
    skip, limit = pagination
    rows = []
    if cabin_id:
        rows = (
            db.query(orm_models.Review)
            .filter(orm_models.Review.cabin_id == int(cabin_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
    elif user_id:
        rows = (
            db.query(orm_models.Review)
            .filter(orm_models.Review.user_id == int(user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
    encoded_rows = jsonable_encoder(rows)
    response = {
        "items": encoded_rows,
        "total": len(encoded_rows),
        "page": skip // limit + 1,
        "size": limit,
    }
    return response
