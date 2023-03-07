import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from db import engine
from models.orm_models import Base
from routers.photo_router import router as photo_router
from routers.cabin_router import router as cabin_router
from routers.booking_router import router as booking_router

Base.metadata.create_all(bind=engine)   # creates all the tables, will not attempt to recreate if they exist

app = FastAPI(docs_url="/")
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(photo_router)
app.include_router(cabin_router)
app.include_router(booking_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
