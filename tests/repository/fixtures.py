import secrets

import pytest
from sqlalchemy import create_engine
from models.orm_models import Base
from sqlalchemy.orm import sessionmaker, declarative_base

from db import get_db_url
from repository.photo_repository import PhotoRepository


@pytest.fixture
def database():
    """before yield => setup(); after yield => teardown()"""
    url = get_db_url(database="postgres")  # connect to the postgres default db
    engine = create_engine(url)
    conn = engine.connect()

    # generate a random string to be used as the name of the test db
    random_db_name = secrets.token_hex(5)
    conn.execute("commit")  # don't delete this else db creation fails
    conn.execute(f'create database "{random_db_name}"')
    conn.execute("commit")
    random_db_engine = create_engine(get_db_url(database=random_db_name))
    Base.metadata.create_all(bind=random_db_engine)

    SessionLocal = sessionmaker(  # get a session make object for the created db
        autocommit=False,
        autoflush=False,
        bind=random_db_engine,
    )
    db = SessionLocal()  # use the session maker to get a session to the test db

    yield db  # return the session to the fixtures/tests that will use it

    random_db_engine.dispose()  # if we dont do this, db drop fails bcs 1 session is left hanging
    db.close()
    # teardown phase, close session
    terminate_connections = f"""
    SELECT *, pg_terminate_backend(pid)
    FROM pg_stat_activity 
    WHERE pid <> pg_backend_pid()
    AND datname = '{random_db_name}';
    """
    conn.execute(terminate_connections)  # drop test database
    conn.execute(f'drop database "{random_db_name}"')  # drop test database
    conn.execute("commit")
    conn.close()  # close connection


@pytest.fixture()
def photo_repository(database):
    return PhotoRepository(database)
