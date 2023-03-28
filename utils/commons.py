from fastapi import Query


def pagination_params(page: int = Query(default=1, gt=0), size: int = Query(default=10, gt=0)):
    return (page - 1) * size, size