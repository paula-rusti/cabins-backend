import uvicorn
from fastapi import FastAPI

app = FastAPI(docs_url="/")


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)