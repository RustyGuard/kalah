import jwt
from sqlalchemy.orm import Session

from src.models import Player

AUTH_SECRET_KEY = "adasdlkasdaksd"


def create_player(session: Session, user_name: str, avatar_id: int) -> str:
    user = Player()
    user.nickname = user_name
    user.avatar_id = avatar_id
    session.add(user)
    session.commit()
    return _create_auth_token(user_name, avatar_id)


def _create_auth_token(user_name: str, avatar_id: int) -> str:
    payload = {
        "user_name": user_name,
        "avatar_id": avatar_id,
    }
    return jwt.encode(payload, AUTH_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str):
    payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
    return payload
