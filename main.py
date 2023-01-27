import datetime

import uvicorn
from fastapi import FastAPI
from db import get_db_session
from models.cabins import User, Role, Cabin

app = FastAPI(docs_url="/")



if __name__ == '__main__':
    # uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    # add_dummy_user()
    # add a cabin to db
    get_db_session().add(Cabin(0, ))
