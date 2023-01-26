import datetime

import uvicorn
from fastapi import FastAPI
from db import get_db_session
from models.user_models import UserModel, Role

app = FastAPI(docs_url="/")


def add_dummy_user():
    # for dev purposes, called only to get a dummy user to bind all cabins to it
    session = get_db_session()
    session.add(
        UserModel(id=0, username="ipopescu", full_name="Ion Popescu", created=datetime.datetime.now(), deleted=False,
                  role=Role.owner))
    session.commit()


if __name__ == '__main__':
    # uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    add_dummy_user()
