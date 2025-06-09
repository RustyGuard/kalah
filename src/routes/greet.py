from fastapi import APIRouter, Depends, Request, Response

from src.routes.auth import auth_required
from src.templates import templates

greet_router = APIRouter(
    dependencies=[
        Depends(auth_required),
    ]
)


@greet_router.get("/")
def main_page(request: Request, user: dict = Depends(auth_required)) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="main_page.html",
        context={
            "avatar_url": request.url_for(
                "static", path=f"images/avatars/avatar{user['avatar_id']}.svg"
            ),
            "user_name": user["user_name"],
        },
    )


@greet_router.get("/settings")
def settings_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={},
    )
