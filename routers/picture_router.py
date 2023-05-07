from fastapi import APIRouter, UploadFile, Depends, Query
from starlette.responses import Response

import models.dto_models
from utils.db import get_db
from repository.photo_repository import PhotoRepository


def photo_repository(db=Depends(get_db)):
    return PhotoRepository(db=db)


router = APIRouter(prefix="/pictures", tags=["pictures"])


@router.post("")
def upload_picture(
    file: UploadFile,
    cabin_id: str,
    principal: str = False,
    photo_repo=Depends(photo_repository),
):
    """uploads a photo of a corresponding cabin"""
    photo_entry = models.dto_models.PhotoIn(
        cabin_id=cabin_id, content=file.file.read(), principal=principal
    )
    photo_repo.add(photo_entry)
    return {"filename": file.filename, "cabin_id": cabin_id}


@router.get("/{id}")
def get_photo(id: int, picture_repo=Depends(photo_repository)):
    """retrieves a photo having a specific id"""
    photo = picture_repo.get_by_id(id)
    if photo is None:
        return Response(status_code=404, content="Not Found")
    return Response(
        status_code=200, content=photo.content, headers={"Content-Type": "image/jpeg"}
    )


@router.get("")
def get_photos_of_cabin(cabin_id: int = Query(None), photo_repo=Depends(photo_repository)):
    """gets a list of photo ids and principal corresponding to a cabin"""
    photos = photo_repo.get_by_cabin(cabin_id)
    return photos
