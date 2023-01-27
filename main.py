import uvicorn
from fastapi import FastAPI

from scripts import read_data

app = FastAPI(docs_url="/")


@app.get("/cabins")
def get_cabins():
    cabins = read_data.get_cabins()
    return cabins


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
