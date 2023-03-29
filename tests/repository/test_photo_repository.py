from sqlalchemy import insert, select

from models.dto_models import PhotoIn
from models.orm_models import Role, User, Cabin, Photo
from tests.repository.fixtures import photo_repository, database

def test_add_photo(photo_repository):
    # 1. Setup - faci setup la mockuri, clase, si variabile
    # 2. Test - apelezi codul de test, salvezi rezultatul
    # 3. Assert - aici faci asset

    # insert the necessary rows as dependencies
    statement = insert(User).values(
        role=Role.owner,
        username="test_user",
        full_name="Test User",
        email_address="email@gmail.com",
        phone_number="0736382028",
        about_me="Some things about me..",
        profile_pic=None,
    ).returning(User.id)
    user_id = photo_repository.db.execute(statement).first()[0]
    photo_repository.db.commit()

    statement = insert(Cabin).values(
        user_id=user_id,
        name="Test Cabin",
        description="Dummy description",
        location="Dummy location",
        facilities=None,
        price=100,
        capacity=2,
        nr_beds=1,
        nr_rooms=1,
        nr_bathrooms=1

    ).returning(Cabin.id)
    cabin_id = photo_repository.db.execute(statement).first()[0]
    photo_repository.db.commit()

    # call the function to be tested
    test_photo = PhotoIn(cabin_id=cabin_id, content=bytearray(), principal=False)
    test_photo_row_id = photo_repository.add(test_photo)

    # select from the db so we can make the assert
    get_inserted_photo_statement = select(Photo).where(Photo.id == test_photo_row_id)
    retrieved_photo = photo_repository.db.execute(get_inserted_photo_statement).first()[0]

    assert retrieved_photo.id == test_photo_row_id


