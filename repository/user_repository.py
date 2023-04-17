import typing

from sqlalchemy import text, insert
from sqlalchemy.orm import Session

from models.orm_models import User
from models.dto_models import UserRegister


class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id_and_role(self, id: int, role: str) -> typing.Optional[User]:
        user = self.db.query(User).filter(User.id == id, User.role == role).first()
        if user:
            return user
        return None

    def get_user_id_by_email_or_username_and_role(
        self, username: str, email: str, role: str
    ) -> typing.Optional[User]:
        statement = text(
            """SELECT * from "user" WHERE (username = :username OR email_address = :email) AND role = :role"""
        ).bindparams(
            username=username,
            email=email,
            role=role,
        )
        user = self.db.execute(statement).first()
        if user:
            return user[0]
        return None

    def insert_user(self, user: UserRegister):
        statement = insert(User).values(
            role=user.role,
            username=user.username,
            password_hash=user.password_hash,
            full_name=user.full_name,
            email_address=user.email,
            phone_number=user.phone_number,
            about_me="",
        )
        self.db.execute(statement=statement)
        self.db.commit()
