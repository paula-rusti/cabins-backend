from sqlmodel import select

from db import get_db_session
from models.tables import User, CabinTable


def get_user():
    with get_db_session() as session:
        statement = select(User)  # select *
        results = session.execute(statement)
        for user in results:
            print(f"userid {user[0].id}")
            print(f"userid {user[0].username}")
            for cabin in user[0].cabins:
                print(cabin)


def get_cabins():
    with get_db_session() as session:
        statement = select(CabinTable)  # select * from cabins
        cabins = session.execute(statement)
        cabins_list = []
        for c in cabins:
            cabins_list.append(c[0])
        return cabins_list


if __name__ == "__main__":
    # get_user()
    cabins = get_cabins()
    print(cabins)
