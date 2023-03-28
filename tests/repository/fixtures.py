import secrets

import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from db import get_db_url
from repository.photo_repository import PhotoRepository


@pytest.fixture
def database():
    random_db_name = secrets.token_hex(5)
    url = get_db_url(database="postgres")
    engine = create_engine(url)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f'create database "{random_db_name}"')
    conn.execute("commit")
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=create_engine(get_db_url(database=random_db_name)),
    )
    db = SessionLocal()
    yield db
    db.close()
    conn.execute(f'drop database "{random_db_name}"')
    conn.execute("commit")
    conn.close()


@pytest.fixture()
def photo_repository(database):
    return PhotoRepository(database)
