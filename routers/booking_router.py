from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models.orm_models
from utils.db import get_db
import models.dto_models, models.orm_models

router = APIRouter(prefix="/bookings", tags=["bookings"])
# route order matters, wildcards should be placed last


@router.post("/add")
def add_booking(
    booking: models.dto_models.BookingCreate, db: Session = Depends(get_db)
):
    to_add = models.orm_models.Booking(**booking.dict())
    db.add(to_add)
    db.commit()
