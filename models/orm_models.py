# models used by the orm
import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Enum,
    func,
    DateTime,
    Boolean,
    SMALLINT,
    Date,
)
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA
from sqlalchemy.orm import relationship

from utils.db import Base


class Role(enum.Enum):
    owner = "owner"
    tourist = "tourist"


class Cabin(Base):
    __tablename__ = "cabin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(50), index=True, nullable=False)
    description = Column(String(500))
    location = Column(String(100), nullable=False)
    facilities = Column(ARRAY(Integer))
    price = Column(Float, nullable=False)
    capacity = Column(SMALLINT, nullable=False)
    nr_beds = Column(SMALLINT, nullable=False)
    nr_rooms = Column(SMALLINT, nullable=False)
    nr_bathrooms = Column(SMALLINT, nullable=False)

    owner = relationship("User", back_populates="cabins")
    photos = relationship("Photo")


# profile + account = user
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(Role))
    username = Column(String(50))
    full_name = Column(String(50))  # separated by spaces
    email_address = Column(String(50))  # needs validation
    password_hash = Column(String(50))
    phone_number = Column(String(15))
    about_me = Column(String(500))
    profile_pic = Column(BYTEA)
    created = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # calculate timestamp on server side
    deleted = Column(Boolean, default=False, nullable=False)

    cabins = relationship("Cabin", back_populates="owner")


class Photo(Base):
    # a table representing photos of cabins
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True, index=True)
    cabin_id = Column(Integer, ForeignKey("cabin.id"), nullable=False)
    content = Column(BYTEA)
    principal = Column(Boolean, nullable=False)     # gonna be ignored and eventually removed from the model


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, index=True)
    cabin_id = Column(Integer, ForeignKey("cabin.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    nr_guests = Column(Integer)


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    cabin_id = Column(Integer, ForeignKey("cabin.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("booking.id"), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    grade = Column(SMALLINT, nullable=False)
    description = Column(String(2000))
