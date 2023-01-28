from sqlmodel import select, Session

from db import get_db_session, get_engine
from models.tables import User, Cabin


def get_user():
    session = get_db_session()
    statement = select(User)    # select *

    results = session.execute(statement)
    temp = results.scalars().all()
    for user in results:
        print(f'userid {user[0].id}')
        print(f'userid {user[0].username}')
        for cabin in user[0].cabins:
            print(cabin)


def get_cabins():
    session = get_db_session()
    statement = select(Cabin)   # select * from cabins
    cabins = session.execute(statement)
    cabins_list = []
    for c in cabins:
        cabins_list.append(c[0])
    return cabins_list


if __name__ == '__main__':
    # get_user()
    cabins = get_cabins()
    print(cabins)