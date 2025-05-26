from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.core.config import settings
from src.database import get_session
from src.logic.auth import create_player, decode_access_token
from src.templates import templates

auth_router = APIRouter()


@auth_router.get("/auth")
def authorize_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={"avatars": [{"id": i} for i in range(settings.AVATARS_COUNT)]},
    )


class AuthError(Exception):
    pass


def auth_required(request: Request):
    access_token = request.cookies.get(settings.AUTH_COOKIE_NAME)
    if access_token is None:
        raise AuthError
    payload = decode_access_token(access_token)
    return payload


@auth_router.post("/auth")
def authorize_user(
    session: Annotated[Session, Depends(get_session)],
    user_name: Annotated[str, Form()],
    avatar_id: Annotated[int, Form()],
) -> Response:
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    auth_token = create_player(session, user_name, avatar_id)
    response.set_cookie(
        settings.AUTH_COOKIE_NAME,
        value=auth_token,
        expires=settings.AUTH_COOKIE_LIFETIME_SECONDS,
        httponly=True,
        samesite="strict",
    )
    return response


@auth_router.get("/exit")
def exit_user() -> Response:
    response = RedirectResponse("/auth")
    response.delete_cookie(
        settings.AUTH_COOKIE_NAME,
        httponly=True,
        samesite="strict",
    )
    return response
