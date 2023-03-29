from sqlalchemy import insert, select

from models.orm_models import Role, User, Cabin, Photo


def test_add_photo(photo_repository):
    # 1. Setup - faci setup la mockuri, clase, si variabile
    # 2. Test - apelezi codul de test, salvezi rezultatul
    # 3. Assert - aici faci asset

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

    statement = insert(Photo).values(
        cabin_id=cabin_id,
        content=None,
        principal=False,
    ).returning(Photo.id)
    photo_id = photo_repository.db.execute(statement).first()[0]
    photo_repository.db.commit()

    get_inserted_photo_statement = select(Photo).where(Photo.id == photo_id)
    retrieved_photo = photo_repository.db.execute(get_inserted_photo_statement).first()[0]

    assert retrieved_photo.id == photo_id


