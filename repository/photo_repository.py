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
            return results.first()