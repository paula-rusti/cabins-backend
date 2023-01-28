from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import add_pagination, paginate, Page
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from models.models import CabinBase
from scripts import read_data

app = FastAPI(docs_url="/")
add_pagination(app)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # maybe write to db here
    pass


@app.get("/cabins", response_model=Page[CabinBase])
def get_cabins():
    # TODO: make query using skip(offset) and limit instead of select *
    cabins_rows = read_data.get_cabins()
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
