import pytest
from sqlalchemy import insert, select

from models.dto_models import CabinIn
from models.orm_models import User, Role, Cabin
from tests.repository.fixtures import cabin_repository, database


@pytest.fixture
def setup(cabin_repository):
    statement = (
        insert(User)
        .values(
            role=Role.owner,
            username="test_user",
            full_name="Test User",
            email_address="email@gmail.com",
            phone_number="0736382028",
            about_me="Some things about me..",
            profile_pic=None,
        )
        .returning(User.id)
    )
    cabin_repository.db.execute(statement).first()
    cabin_repository.db.commit()


def test_add_photo(cabin_repository, setup):
    # call the function to be tested
    test_cabin = CabinIn(
        user_id=None,
        name="Test Cabin",
        description="Dummy description",
        location="Dummy location",
        price=100,
        facilities=[],
        capacity=5,
        nr_beds=3,
        nr_rooms=3,
        nr_bathrooms=2,
    )
    test_cabin_row_id = cabin_repository.add(test_cabin, user_id=1)

    # select from the db so we can make the assert
    get_inserted_cabin_statement = select(Cabin).where(Cabin.id == test_cabin_row_id)
    retrieved_cabin = cabin_repository.db.execute(get_inserted_cabin_statement).first()[
        0
    ]

    assert retrieved_cabin.id == test_cabin_row_id
