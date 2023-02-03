from fastapi import APIRouter, UploadFile, Depends
from starlette.responses import Response

from db import get_db_session
from repository.photo_repository import PhotoRepository

from models.tables import Photo


def photo_repository():
    return PhotoRepository(session=get_db_session())


router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/{cabin_id}/add")
def upload_picture(
        file: UploadFile, cabin_id: str, principal: str = False, photo_repo=Depends(photo_repository)
):
    """uploads a photo of a corresponding cabin"""
    photo_entry = Photo(cabin_id=cabin_id, content=file.file.read(), principal=principal)
    photo_repo.add(photo_entry)
    return {"filename": file.filename, "cabin_id": cabin_id}


@router.get("/{id}")
def get_photo(id: int, photo_repo=Depends(photo_repository)):
    """retrieves a photo having a specific id"""
    photo = photo_repo.get_by_id(id)
    if photo is None:
        return Response(status_code=404, content="Not Found")
    return Response(status_code=200, content=photo.content, headers={"Content-Type": "image/jpeg"})


@router.get("/cabin/{cabin_id}")
def get_photos_of_cabin(cabin_id: int, photo_repo=Depends(photo_repository)):
    """gets a list of photo ids corresponding to a cabin"""
    ids = photo_repo.get_photos_of_cabin(cabin_id)
    return ids


@router.get("/cabin/principal/{cabin_id}")
def get_principal_photo_of_cabin(cabin_id: int, photo_repo=Depends(photo_repository)):
    photo = photo_repo.get_principal(cabin_id)
    if photo is None:
        return Response(status_code=404, content="Not Found")
    return Response(status_code=200, content=photo.content, headers={"Content-Type": "image/jpeg"})
