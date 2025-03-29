from typing import Annotated

from fastapi import APIRouter, Form, Request, Response, status
from fastapi.responses import RedirectResponse

from logic.auth import create_auth_token, decode_access_token
from templates import templates

AVATARS_COUNT = 10

auth_router = APIRouter()


@auth_router.get("/auth")
def authorize_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={"avatars": [{"id": i} for i in range(AVATARS_COUNT)]},
    )


AUTH_COOKIE_LIFETIME_SECONDS = 30 * 60
AUTH_COOKIE_NAME = "access_token"


class AuthError(Exception):
    pass


def auth_required(request: Request):
    access_token = request.cookies.get(AUTH_COOKIE_NAME)
    if access_token is None:
        raise AuthError
    payload = decode_access_token(access_token)
    return payload


@auth_router.post("/auth")
def authorize_user(
    user_name: Annotated[str, Form()],
    avatar_id: Annotated[int, Form()],
) -> Response:
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    auth_token = create_auth_token(user_name, avatar_id)
    response.set_cookie(
        AUTH_COOKIE_NAME,
        value=auth_token,
        expires=AUTH_COOKIE_LIFETIME_SECONDS,
        httponly=True,
        samesite="strict",
    )
    return response


@auth_router.get("/exit")
def exit_user() -> Response:
    response = RedirectResponse("/auth")
    response.delete_cookie(
        AUTH_COOKIE_NAME,
        httponly=True,
        samesite="strict",
    )
    return response
