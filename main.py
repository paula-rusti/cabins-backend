import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils.db import engine
from models.orm_models import Base
from routers.booking_router import router as booking_router
from routers.cabin_router import router as cabin_router
from routers.photo_router import router as photo_router
from routers.review_router import router as review_router
from routers.user_router import router as user_router

Base.metadata.create_all(
    bind=engine
)  # creates all the tables, will not attempt to recreate if they exist


def create_app():
    app = FastAPI(docs_url="/")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user_router)
    app.include_router(cabin_router)
    app.include_router(photo_router)
    app.include_router(booking_router)
    app.include_router(review_router)
    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", host="localhost", port=8000, reload=True)
