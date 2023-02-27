from functools import lru_cache

from sqlmodel import create_engine, SQLModel
from sqlmodel import Session

user = "app"
password = "app"
host = "localhost"
port = 5432
database = "mydbname"

url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)


@lru_cache()
def get_engine():
    engine = create_engine(url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


def get_db_session():
    engine = get_engine()
    session = Session(bind=engine)
    return session


# slowly replace sqlmodel with sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(url)
# encourage placing configuration options for creating new Session objects in just one place
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# models package will import it
Base = declarative_base()   # orm models will inherit from it, keeps metadata in one place

# will be used as a dependency in routers to interact with the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
