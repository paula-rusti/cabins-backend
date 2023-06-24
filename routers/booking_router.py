from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

import models.dto_models
import models.orm_models
from repository.booking_repository import BookingRepository
from utils.db import get_db

http_bearer = HTTPBearer()

router = APIRouter(prefix="/bookings", tags=["bookings"])
# route order matters, wildcards should be placed last

def bookings_repository(db=Depends(get_db)):
    return BookingRepository(db=db)


# all methods which add an entry shall return its id
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


@router.get("/{_id}")
def get_booking(
    _id: int, repo: BookingRepository = Depends(bookings_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return repo.get_booking(_id)

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

@router.get("/owner/")
def get_bookings_of_owner(
    skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository),
    authorize: AuthJWT = Depends(), token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    role = authorize.get_raw_jwt().get("role")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if role != "owner":
        raise HTTPException(status_code=401, detail="User is not a owner")
    return repo.get_bookings_of_owner(user_id, skip, limit)