import jwt

AUTH_SECRET_KEY = "adasdlkasdaksd"


def create_auth_token(user_name: str, avatar_id: int) -> str:
    payload = {
        "user_name": user_name,
        "avatar_id": avatar_id,
    }
    return jwt.encode(payload, AUTH_SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str):
    payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
    return payload
