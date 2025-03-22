from fastapi import Request, Response
from pydantic import BaseModel

from templates import templates


def authorize_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={},
    )


class AuthData(BaseModel):
    user_name: str
    avatar_id: int


def authorize_user(request: Request, data: AuthData) -> Response:
    raise NotImplementedError
