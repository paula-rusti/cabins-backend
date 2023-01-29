from sqlalchemy.sql.functions import count
from sqlmodel import select

from models.tables import Cabin
from repository.repository import AbstractCabinsRepository


class CabinsRepository(AbstractCabinsRepository):
    def __init__(self, session):
        self.session = session

    def add(self, cabin):
        with self.session as session:
            session.add(cabin)

    def get(self, reference):
        # reference should be an object of type {Cabin.field_name: cabin_field_value}
        with self.session as session:
            statement = select(Cabin).where(Cabin.location == reference)
            results = session.execute(statement)
            cabin_list = []
            for cabin in results:
                cabin_list.append(cabin[0])
            return cabin_list

    def get_all(self):
        statement = select(Cabin)  # select * from cabins
        with self.session as session:
            cabins = session.execute(statement)
            cabins_list = []
            for c in cabins:
                cabins_list.append(c[0])
            return cabins_list

    def get_count(self):
        with self.session as session:
            cnt = session.query(Cabin).count()
            return cnt
