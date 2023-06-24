import datetime

from fastapi import APIRouter, Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from passlib.context import CryptContext


import models.orm_models
from models.dto_models import UserLogin, UserRegister, MessageResponse
from repository.user_repository import UsersRepository
from utils.db import get_db

router = APIRouter(prefix="/users", tags=["users"])
# route order matters, wildcards should be placed last

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

http_bearer = HTTPBearer()

@router.get("/me")
def get_current_user(authorize: AuthJWT = Depends(), token=Depends(http_bearer)):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user_email": current_user, "properties": authorize.get_raw_jwt()}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

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
    user.password = get_password_hash(user.password)
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
        if not verify_password(user.password, db_user.password):
            return JSONResponse(
                status_code=401,
                content=jsonable_encoder(MessageResponse(message="Login failed.")),
            )
        expires = datetime.timedelta(days=30)
        access_token = authorize.create_access_token(subject=user.email, expires_time=expires, user_claims={
            "role": user.role,
            "user_id": db_user_id,
        })
        refresh_token = authorize.create_refresh_token(subject=user.email)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
    # login failed
    return JSONResponse(
        status_code=401,
        content=jsonable_encoder(MessageResponse(message="Login failed.")),
    )


@router.put("/{username}/description", response_model=MessageResponse)
def update_user_description(username: str, description: str, db: Session = Depends(get_db)):
    db_user = db.query(models.orm_models.User).filter(models.orm_models.User.username == username).first()
    if db_user is None:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                MessageResponse(
                    message="User with given username does not exist."
                )
            ),
        )
    db_user.about_me = description
    db.commit()
    return MessageResponse(message="User description updated.")


@router.put("/{username}/profile_picture", response_model=MessageResponse)
def update_user_profile_picture(username: str, profile_picture: UploadFile, db: Session = Depends(get_db)):
    db_user = db.query(models.orm_models.User).filter(models.orm_models.User.username == username).first()
    if db_user is None:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                MessageResponse(
                    message="User with given username does not exist."
                )
            ),
        )
    db_user.profile_pic = profile_picture.file.read()
    db.commit()
    return MessageResponse(message="User profile picture updated.")