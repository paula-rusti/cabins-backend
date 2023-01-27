import datetime

from db import get_db_session
from models.cabins import User, Role, Cabin, Facility


def add_dummy_user():
    # for dev purposes, called only to get a dummy user to bind all cabins to it
    session = get_db_session()
    session.add(
        User(
            id=0,
            username="ipopescu",
            full_name="Ion Popescu",
            created=datetime.datetime.now(),
            deleted=False,
            role=Role.owner,
        )
    )
    session.commit()


def add_cabin():
    session = get_db_session()
    session.add(
        Cabin(
            user_id=0,
            name="Cabana2",
            price=100,
            location="Arad",
            description="description",
            photos=[
                "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
                "https://cdn.vuetifyjs.com/images/cards/hotel.jpg",
                "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg",
            ],
            facilities=[Facility.air_conditioning, Facility.towels, Facility.towels],
        )
    )
    session.commit()


if __name__ == "__main__":
    # add_dummy_user()
    add_cabin()
