from functools import lru_cache

from sqlmodel import create_engine, SQLModel
from sqlmodel import Session

user = 'app'
password = 'app'
host = 'localhost'
port = 5432
database = 'mydbname'

url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database
)


@lru_cache()
def get_engine():
    engine = create_engine(url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


@lru_cache()
def get_db_session():
    engine = get_engine()
    session = Session(bind=engine)
    return session
