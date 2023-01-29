from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination, paginate, Page
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from db import get_db_session
from models.models import CabinBase
from repository.cabins_repository import CabinsRepository

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


@app.get("/cabins", response_model=Page[CabinBase])
def get_cabins(location: Optional[str] = None, cabins_repo: CabinsRepository = Depends(cabins_repository)):
    # TODO: make query using skip(offset) and limit instead of select *
    cabins_rows = []
    if not location:
        cabins_rows = cabins_repo.get_all()
    else:
        cabins_rows = cabins_repo.get(reference=location)
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
