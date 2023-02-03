from sqlmodel import select

from models.tables import Photo
from repository.repository import AbstractPhotoRepository


class PhotoRepository(AbstractPhotoRepository):
    def __init__(self, session):
        self.session = session

    def add(self, photo):
        with self.session as session:
            session.add(photo)
            session.commit()

    def get_by_id(self, id):
        statement = select(Photo).where(Photo.id == int(id))
        with self.session as session:
            results = session.execute(statement)
            return results.first()[0]

    def get_photos_of_cabin(self, cabin_id):
        statement = select(Photo).where(Photo.cabin_id == int(cabin_id))
        with self.session as session:
            results = session.execute(statement)
            id_list = []
            for c in results:
                id_list.append(c[0].id)
            return id_list

    def get_principal(self, cabin_id):
        statement = select(Photo).where(Photo.cabin_id == int(cabin_id)).where(Photo.principal == True)
        with self.session as session:
            results = session.execute(statement).first()
            if results is not None:
                return results[0]
            else:
                return None
