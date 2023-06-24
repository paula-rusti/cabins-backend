import datetime
import sys
from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from starlette.responses import JSONResponse

from utils.db import get_db
from models.dto_models import CabinIn
from repository.cabins_repository import CabinsRepository
from utils.commons import pagination_params

router = APIRouter(prefix="/cabins", tags=["cabins"])
http_bearer = HTTPBearer()


# route order matters, wildcards should be placed last
def cabins_repository(db=Depends(get_db)):
    return CabinsRepository(db=db)


@router.get("")
def retrieve_cabins(
    user_id: int = Query(None),
    location: Optional[str] = Query(None),
    capacity: Optional[int] = Query(None),
    rating: Optional[int] = Query(None),
    start_date: Optional[datetime.date] = Query(None),  # datetime.date.today
    end_date: Optional[datetime.date] = Query(None),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    has_facility: Optional[List[str]] = Query(None),
    pagination=Depends(pagination_params),
    cabins_repo: CabinsRepository = Depends(cabins_repository),
):
    skip, limit = pagination

    if not (
        user_id
        or location
        or capacity
        or rating
        or start_date
        or end_date
        or has_facility
        or min_price
        or max_price
    ):  # retrieve all cabins
        cabin_rows = cabins_repo.get_all(skip, limit)
    else:  # filtered search
        cabin_rows = cabins_repo.get_filtered_cabins(
            user_id,
            location,
            capacity,
            rating,
            start_date,
            end_date,
            min_price,
            max_price,
            has_facility,
            skip,
            limit,
        )

    encoded_rows = jsonable_encoder(cabin_rows)
    response = {
        "items": encoded_rows,
        "total": len(encoded_rows),
        "page": skip // limit + 1,
        "size": limit,
    }
    return JSONResponse(status_code=200, content=response)


@router.post("")
def add_cabin(
    cabin: CabinIn,
    cabins_repo: CabinsRepository = Depends(cabins_repository),
    authorize: AuthJWT = Depends(),
    token=Depends(http_bearer)
):
    authorize.jwt_required()
    user_id = authorize.get_raw_jwt().get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        cabin_id = cabins_repo.add(cabin, user_id)  # user_id is taken from header
    except Exception:
        type, value, traceback = sys.exc_info()
        detail = value.args[0]
        raise HTTPException(status_code=500, detail=f"Error: {detail}")
    return JSONResponse(status_code=200, content={"cabin_id": cabin_id})


@router.get("/count")
def get_cabins_count(cabins_repo: CabinsRepository = Depends(cabins_repository)):
    cnt = cabins_repo.get_count()
    return cnt


@router.get("/{id}")
def get_cabin_by_id(
    id: int, cabins_repo: CabinsRepository = Depends(cabins_repository)
):
    try:
        cabin = cabins_repo.get_by_id(id)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")
    else:
        return cabin
