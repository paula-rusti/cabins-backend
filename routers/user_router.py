from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import models.orm_models
from models.dto_models import UserLogin, UserRegister, MessageResponse
from repository.user_repository import UsersRepository
from utils.db import get_db

router = APIRouter(prefix="/users", tags=["users"])
# route order matters, wildcards should be placed last


@AuthJWT.load_config
class AuthJwtSettings(BaseModel):
    authjwt_secret_key: str = "b9860792c61051d3640518642ac5ea"


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


def users_repository(db=Depends(get_db)):
    return UsersRepository(db=db)


@router.get("/")
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.orm_models.User).offset(skip).limit(limit).all()


@router.post("/register", response_model=MessageResponse)
def register_user(
    user: UserRegister, repo: UsersRepository = Depends(users_repository)
):
    db_user = repo.get_user_id_by_email_or_username_and_role(
        user.username, user.email, user.role
    )
    if db_user is not None:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                MessageResponse(
                    message="User with email or username already registered for given role."
                )
            ),
        )

    repo.insert_user(user)
    return MessageResponse(message="User registered")


@router.post("/login", response_model=LoginResponse)
def login_user(
    user: UserLogin,
    repo: UsersRepository = Depends(users_repository),
    authorize: AuthJWT = Depends(),
):
    db_user_id = repo.get_user_id_by_email_or_username_and_role(
        "", user.email, user.role
    )
    db_user = repo.get_user_by_id_and_role(db_user_id, user.role)
    if db_user:
        if db_user.password_hash != user.password_hash:
            return JSONResponse(
                status_code=401,
                content=jsonable_encoder(MessageResponse(message="Login failed.")),
            )
        access_token = authorize.create_access_token(subject=user.email)
        refresh_token = authorize.create_refresh_token(subject=user.email)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
    # login failed
    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(MessageResponse(message="Login failed.")),
    )
