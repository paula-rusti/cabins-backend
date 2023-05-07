from sqlalchemy import insert
from sqlalchemy.orm import Session

from models import dto_models, orm_models
from models.orm_models import Photo
from repository.repository import AbstractPhotoRepository


class PhotoRepository(AbstractPhotoRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, photo: dto_models.PhotoIn):
        statement = (
            insert(Photo)
            .values(
                cabin_id=photo.cabin_id,
                content=photo.content,
                principal=photo.principal,
            )
            .returning(Photo.id)
        )
        photo_id = self.db.execute(statement).first()[0]
        self.db.commit()
        return photo_id

    def get_by_id(self, id):
        return (
            self.db.query(orm_models.Photo)
            .filter(orm_models.Photo.id == int(id))
            .first()
        )

    def get_photos_of_cabin(self, cabin_id):
        # returns photos of a certain cabin sorted by principal first
        # format arr[{id: int, principal: bool}]
        results = (
            self.db.query(orm_models.Photo)
            .filter(orm_models.Photo.cabin_id == int(cabin_id))
            .all()
        )
        photos = [{"id": p.id, "principal": p.principal} for p in results]
        photos.sort(key=lambda x: x["principal"], reverse=True)
        return photos
