import random

import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.models import Player


def _gen_unique_user_name(user_name: str) -> str:
    return f"{user_name}@{random.randint(1, 9999):04d}"


def create_player(session: Session, user_name: str, avatar_id: int) -> str:
    user_name = _gen_unique_user_name(user_name)
    user = Player()
    user.nickname = user_name
    user.avatar_id = avatar_id
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    return _create_auth_token(user_name, avatar_id)


def _create_auth_token(user_name: str, avatar_id: int) -> str:
    payload = {
        "user_name": user_name,
        "avatar_id": avatar_id,
    }
    return jwt.encode(payload, settings.AUTH_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str):
    payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=["HS256"])
    return payload
