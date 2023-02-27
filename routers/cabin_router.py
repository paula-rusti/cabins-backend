from typing import Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import paginate, Page
from starlette.responses import JSONResponse

from db import get_db_session
from models.models import CabinBase
from repository.cabins_repository import CabinsRepository, CabinFilters

router = APIRouter(prefix="/cabins", tags=["cabins"])


def cabins_repository():
    return CabinsRepository(session=get_db_session())


@router.get("/", response_model=Page[CabinBase])
def get_cabins(
        location: Optional[List[str]] = Query([], description="Cabin location"),
        price_low: Optional[int] = Query(0, description="Cabin price"),
        price_high: Optional[int] = Query(2 ** 53, description="Cabin price"),
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
    cabins_page = paginate(cabins_rows)
    return JSONResponse(status_code=200, content=jsonable_encoder(cabins_page))


@router.get("/count")
def get_total_cabins(cabins_repo: CabinsRepository = Depends(cabins_repository)):
    cnt = cabins_repo.get_count()
    return cnt


@router.get("/{id}")
def get_cabin(id: int, cabins_repo: CabinsRepository = Depends(cabins_repository)):
    try:
        cabin = cabins_repo.get_cabin_by_id(id)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")
    else:
        return cabin
