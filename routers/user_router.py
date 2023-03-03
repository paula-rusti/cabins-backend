from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models.orm_models
from db import get_db
from repository.cabins_repository import CabinsRepository

router = APIRouter(prefix="/users", tags=["users"])
# route order matters, wildcards should be placed last


def cabins_repository(db=Depends(get_db)):
    return CabinsRepository(session=None, db=db)


@router.get("/")
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.orm_models.User).offset(skip).limit(limit).all()



