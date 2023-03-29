import pytest
from sqlalchemy import insert, select

from models.dto_models import PhotoIn
from models.orm_models import Role, User, Cabin, Photo
from tests.repository.fixtures import photo_repository, database


@pytest.fixture
def setup(photo_repository):
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
    user_id = photo_repository.db.execute(statement).first()[0]
    photo_repository.db.commit()

    statement = (
        insert(Cabin)
        .values(
            user_id=user_id,
            name="Test Cabin",
            description="Dummy description",
            location="Dummy location",
            facilities=None,
            price=100,
            capacity=2,
            nr_beds=1,
            nr_rooms=1,
            nr_bathrooms=1,
        )
        .returning(Cabin.id)
    )
    photo_repository.db.execute(statement).first()
    photo_repository.db.commit()


def test_add_photo(photo_repository, setup):
    # call the function to be tested
    test_photo = PhotoIn(cabin_id=1, content=bytearray(), principal=False)
    test_photo_row_id = photo_repository.add(test_photo)

    # select from the db so we can make the assert
    get_inserted_photo_statement = select(Photo).where(Photo.id == test_photo_row_id)
    retrieved_photo = photo_repository.db.execute(get_inserted_photo_statement).first()[
        0
    ]

    assert retrieved_photo.id == test_photo_row_id


def test_get_photo_by_id(photo_repository, setup):
    """Tests for retrieving both existing and non-existing photos"""
    statement = (
        insert(Photo)
        .values(cabin_id=1, content=bytearray(), principal=False)
        .returning(Photo.id)
    )
    photo_id = photo_repository.db.execute(statement).first()[0]
    photo_repository.db.commit()

    # now try to get the photo with that id
    retrieved_photo = photo_repository.get_by_id(photo_id)
    invalid_photo = photo_repository.get_by_id(
        2
    )  # does not exist in the and the get function should return None
    assert retrieved_photo.id == photo_id
    assert invalid_photo is None


def test_get_photos_of_cabin(photo_repository, setup):
    expected_photos_array = []
    principal = True
    for i in range(1, 3 + 1):   # add 3 photos for cabin 1
        if i % 2 == 0:
            principal = False

        statement = (
            insert(Photo)
            .values(cabin_id=1, content=bytearray(), principal=principal)
            .returning(Photo.id)
        )
        photo_id = photo_repository.db.execute(statement).first()[0]
        expected_photos_array.append({"id": photo_id, "principal": principal})
    photo_repository.db.commit()

    retrieved_photos = photo_repository.get_photos_of_cabin(1)      # arr[{id: int, principal: bool}]
    max_len = max(len(retrieved_photos), len(expected_photos_array))
    for i in range(max_len):
        assert retrieved_photos[i] == expected_photos_array[i]



