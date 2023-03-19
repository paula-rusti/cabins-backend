import dataclasses

from fastapi import Header


@dataclasses.dataclass
class User:
    user_id: int


def authorize_user(user_id: int = Header(...)):
    return User(user_id=user_id)
