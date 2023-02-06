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

    def get_photos_of_cabin(self, cabin_id, principal=False):
        # returns an array of objects containing the photo id and a boolean value specifying if the photo is principal or not
        statement = select(Photo).where(Photo.cabin_id == int(cabin_id))
        with self.session as session:
            results = session.execute(statement)
            photos = [{"id": c[0].id, "principal": c[0].principal} for c in results]
            photos.sort(key=lambda x: x["principal"], reverse=True)
            return photos
