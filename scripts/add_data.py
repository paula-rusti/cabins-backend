import datetime

from db import get_db_session
from models.models import Role, Facility
from models.tables import User, CabinTable


def add_dummy_user():
    # for dev purposes, called only to get a dummy user to bind all cabins to it
    with get_db_session() as session:
        session.add(
            User(
                username="viancu",
                full_name="Vlad Iancu",
                created=datetime.datetime.now(),
                deleted=False,
                role=Role.owner,
            )
        )
        session.commit()


def add_cabin(cabin_name: str):
    with get_db_session() as session:
        session.add(
            CabinTable(
                user_id=0,
                name=cabin_name,
                price=100,
                location="Arad",
                description="description",
                photos=[
                    "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
                    "https://cdn.vuetifyjs.com/images/cards/hotel.jpg",
                    "https://cdn.vuetifyjs.com/images/cards/sunshine.jpg",
                ],
                facilities=[
                    Facility.air_conditioning,
                    Facility.towels,
                    Facility.towels,
                ],
            )
        )
        session.commit()


if __name__ == "__main__":
    # add_dummy_user()
    for name in ["Cabana6", "Cabana7"]:
        add_cabin(name)
