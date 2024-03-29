from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from repository.booking_repository import BookingRepository
from utils.db import get_db
from models import orm_models, dto_models
from repository.review_repository import ReviewRepository
from utils.commons import pagination_params

router = APIRouter(prefix="/reviews", tags=["reviews"])
http_bearer = HTTPBearer()

def review_repository(db=Depends(get_db)):
    return ReviewRepository(db=db)

def booking_repository(db=Depends(get_db)):
    return BookingRepository(db=db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_review(
    review: dto_models.ReviewIn,
    review_repo: ReviewRepository = Depends(review_repository),
    booking_repo: BookingRepository = Depends(booking_repository),
    token: HTTPBearer = Depends(http_bearer),
    auth_jwt: AuthJWT = Depends(),
):
    """
    The review is associated with a booking by the booking id
    This route will be authenticated and the user id is extracted from a header for mocking demo
    """
    auth_jwt.jwt_required()
    user_id = auth_jwt.get_raw_jwt()["user_id"]
    role = auth_jwt.get_raw_jwt()["role"]

    if role != "tourist":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only tourists can add reviews",
        )

    booking_id = review.booking_id
    booking = booking_repo.get_booking(booking_id)
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found, cannot add review",
        )

    if booking.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Booking does not belong to logged in tourist",
        )


    inserted = review_repo.add_review(review=review, user_id=user_id)
    if not inserted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Review cannot be added"
        )
    return {"detail": "Review added"}


@router.get("/{id}")
def get_review(id: int, repo: ReviewRepository = Depends(review_repository)):
    """
    retrieves a review having a specific id
    """
    review = repo.get_review(id)
    if review is None:
        return Response(status_code=404, content="Not Found")
    return review


# TODO test
# TODO add stronger constraint for mutually exclusive query parameters - raise custom exception if not met (bad req)
# TODO use review repository instead of directly session
@router.get("/")
def get_reviews(
    user_id: int = None,
    cabin_ids: List[int] = Query(None),
    booking_id: int = None,
    pagination=Depends(pagination_params),
    db: Session = Depends(get_db),
):
    """
    :param user_id: retrieves all reviews of a user
    :param cabin_ids: retrieves all reviews of a cabin
    :param booking_id: retrieves the review coresponding to a booking_id
    :param pagination:
    :param db:
    :return:
    """
    if not cabin_ids and not user_id and not booking_id:
        raise HTTPException(
            status_code=500,
            detail="Bad Request",
            headers={
                "X-Error": "At least one query param (cabin_ids, user_id, booking_id) must be specified"
            },
        )
    skip, limit = pagination
    rows = []
    if cabin_ids:
        rows = []
        for cabin_id in cabin_ids:
            current_rows = (
                db.query(orm_models.Review)
                .filter(orm_models.Review.cabin_id == int(cabin_id))
                .offset(skip)
                .limit(limit)
                .all()
            )
            rows.append(current_rows)
    elif user_id:
        rows = (
            db.query(orm_models.Review)
            .filter(orm_models.Review.user_id == int(user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
    elif booking_id:
        rows = (
            db.query(orm_models.Review)
            .filter(orm_models.Review.booking_id == int(booking_id))
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
