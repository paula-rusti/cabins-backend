from fastapi import APIRouter, Depends

import models.dto_models
import models.orm_models
from repository.booking_repository import BookingRepository
from utils.db import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])
# route order matters, wildcards should be placed last

def bookings_repository(db=Depends(get_db)):
    return BookingRepository(db=db)


# all methods which add an entry shall return its id
@router.post("/add")
def add_booking(
    booking: models.dto_models.BookingCreate, repo: BookingRepository = Depends(bookings_repository)
):
    return repo.add_booking(booking)


@router.get("/{_id}")
def get_booking(_id: int, repo: BookingRepository = Depends(bookings_repository)):
    return repo.get_booking(_id)

@router.get("/cabin/{cabin_id}")
def get_bookings_of_cabin(
    cabin_id: int, skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository)
):
    return repo.get_bookings_of_cabin(cabin_id, skip, limit)

@router.get("/tourist/{user_id}")
def get_bookings_of_tourist(
    user_id: int, skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository)
):
    return repo.get_bookings_of_tourist(user_id, skip, limit)

@router.get("/owner/{user_id}")
def get_bookings_of_owner(
    user_id: int, skip: int = 0, limit: int = 100, repo: BookingRepository = Depends(bookings_repository)
):
    return repo.get_bookings_of_owner(user_id, skip, limit)