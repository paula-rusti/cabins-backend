from sqlmodel import select, Session

from db import get_db_session, get_engine
from models.cabins import User


def get_user():
    session = get_db_session()
    statement = select(User)    # select *

    results = session.execute(statement)
    for user in results:
        print(f'userid {user[0].id}')
        print(f'userid {user[0].username}')
        for cabin in user[0].cabins:
            print(cabin)


if __name__ == '__main__':
    get_user()
