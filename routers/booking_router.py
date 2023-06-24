from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

import models.dto_models
import models.orm_models
from repository.booking_repository import BookingRepository
from repository.user_repository import UsersRepository
from routers.user_router import users_repository
from utils.db import get_db

http_bearer = HTTPBearer()

router = APIRouter(prefix="/bookings", tags=["bookings"])
# route order matters, wildcards should be placed last

def bookings_repository(db=Depends(get_db)):
    return BookingRepository(db=db)


def process_booking(booking: models.dto_models.Booking, booking_repo, user_repo):

    full_name = user_repo.get_full_name_by_id(booking.user_id)
    cabin_name = booking_repo.get_cabin_name_by_id(booking.cabin_id)

    booking.tourist_name = full_name
    booking.cabin_name = cabin_name

    return booking

# all methods which add an entry shall return its id
# TODO all user_id shall not be in body
@router.post("/add")
def add_booking(
    booking: models.dto_models.BookingCreate, repo: BookingRepository = Depends(bookings_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return repo.add_booking(booking)

@router.get("/cabin/{cabin_id}")
def get_bookings_of_cabin(
    cabin_id: int, skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    role = authorize.get_raw_jwt().get("role")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role != "owner":
        raise HTTPException(status_code=401, detail="User is not a owner")
    return repo.get_bookings_of_cabin(cabin_id, skip, limit)

@router.get("/tourist/")
def get_bookings_of_tourist(
    skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    role = authorize.get_raw_jwt().get("role")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role != "tourist":
        raise HTTPException(status_code=401, detail="User is not a tourist")
    return repo.get_bookings_of_tourist(user_id, skip, limit)

@router.get("/owner")
def get_bookings_of_owner(
    skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer),
    repo_b: BookingRepository = Depends(bookings_repository),
    repo_u: UsersRepository = Depends(users_repository),
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    role = authorize.get_raw_jwt().get("role")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role != "owner":
        raise HTTPException(status_code=401, detail="User is not a owner")
    # todo replace user_id with fullname and cabin_id with cabin name
    arr = repo.get_bookings_of_owner(user_id, skip, limit)
    return list(map(lambda x: process_booking(x, repo_b, repo_u), arr))

@router.get("/{_id}")
def get_booking(
    _id: int, repo: BookingRepository = Depends(bookings_repository),
    user_repo: UsersRepository = Depends(users_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    booking = repo.get_booking(_id)
    return process_booking(booking, repo, user_repo)