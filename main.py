from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Depends, Query, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination, paginate, Page
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from db import get_db_session
from models.models import CabinBase
from models.tables import Photo
from repository.cabins_repository import CabinsRepository, CabinFilters
from repository.photo_repository import PhotoRepository

app = FastAPI(docs_url="/")
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def cabins_repository():
    return CabinsRepository(session=get_db_session())


def photo_repository():
    return PhotoRepository(session=get_db_session())


@app.post("/photos/{cabin_id}/add")
def upload_picture(
    file: UploadFile, cabin_id: str, photo_repo=Depends(photo_repository)
):
    # call method to write picture to db
    photo_entry = Photo(cabin_id=cabin_id, content=file.file.read())
    photo_repo.add(photo_entry)
    return {"filename": file.filename, "cabin_id": cabin_id}


@app.get("/photo/{id}")
def get_photo(id: int, photo_repo=Depends(photo_repository)):
    photo = photo_repo.get_by_id(id)
    if photo is None:
        return Response(status_code=404, content="Not Found")
    return Response(status_code=200, content=photo[0].content, headers={"Content-Type": "image/jpeg"})


@app.get("/cabins", response_model=Page[CabinBase])
def get_cabins(
    location: Optional[List[str]] = Query([], description="Cabin location"),
    price_low: Optional[int] = Query(0, description="Cabin price"),
    price_high: Optional[int] = Query(2**53, description="Cabin price"),
    cabins_repo: CabinsRepository = Depends(cabins_repository),
):
    # TODO: make query using skip(offset) and limit instead of select *
    if not (location or price_low or price_high):
        cabins_rows = cabins_repo.get_all()
    else:
        price = {}
        if price_low is not None:
            price["min"] = price_low
        if price_high is not None:
            price["max"] = price_high
        cabins_rows = cabins_repo.get(
            filters=CabinFilters(location=location, price=price)
        )
    cabins = [
        CabinBase(
            name=cabin.name,
            price=cabin.price,
            location=cabin.location,
            description=cabin.description,
            photos=cabin.photos,
            facilities=cabin.facilities,
        )
        for cabin in cabins_rows
    ]
    cabins_page = paginate(cabins)
    return JSONResponse(status_code=200, content=jsonable_encoder(cabins_page))


@app.get("/cabins/total")
def get_total_cabins(cabins_repo: CabinsRepository = Depends(cabins_repository)):
    cnt = cabins_repo.get_count()
    return cnt


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
