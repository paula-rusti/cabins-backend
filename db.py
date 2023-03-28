from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def get_db_url(
    user="app", password="app", host="localhost", port=5432, database="mydbname"
):
    return "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )


engine = create_engine(get_db_url())
# encourage placing configuration options for creating new Session objects in just one place
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# models package will import it
Base = (
    declarative_base()
)  # orm models will inherit from it, keeps metadata in one place


# will be used as a dependency in routers to interact with the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
