from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models.orm_models
from db import get_db

router = APIRouter(prefix="/users", tags=["users"])
# route order matters, wildcards should be placed last


@router.get("/")
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.orm_models.User).offset(skip).limit(limit).all()
