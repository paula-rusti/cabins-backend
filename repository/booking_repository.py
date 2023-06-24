from sqlalchemy.orm import Session

from models.dto_models import Booking
from models.dto_models import BookingCreate
from models.orm_models import Booking, Cabin
from repository.repository import AbstractBookingRepository


class BookingRepository(AbstractBookingRepository):
    def __init__(self, db: Session):
        self.db = db

    def add_booking(self, booking: BookingCreate):
        to_add = Booking(**booking.dict())
        self.db.add(to_add)
        self.db.commit()
        return to_add

    def get_booking(self, _id):
        return (
            self.db.query(Booking)
            .filter(Booking.id == _id)
            .first()
        )

    def get_bookings_of_cabin(self, cabin_id, skip, limit):
        return (
            self.db.query(Booking)
            .filter(Booking.cabin_id == int(cabin_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_bookings_of_tourist(self, user_id, skip, limit):
        return (
            self.db.query(Booking)
            .filter(Booking.user_id == int(user_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_bookings_of_owner(self, user_id, skip, limit):
        # get all bookings of cabins owned by user
        cabins = self.db.query(Cabin).filter(Cabin.user_id == user_id).all()
        cabin_ids = [cabin.id for cabin in cabins]
        return (
            self.db.query(Booking)
            .filter(Booking.cabin_id.in_(cabin_ids))
            .offset(skip)
            .limit(limit)
            .all()
        )


