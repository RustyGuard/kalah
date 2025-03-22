from typing import Annotated

from fastapi import APIRouter, Form, Request, Response

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


@auth_router.post("/auth")
def authorize_user(
    request: Request,
    user_name: Annotated[str, Form()],
    avatar_id: Annotated[int, Form()],
) -> Response:
    raise NotImplementedError
