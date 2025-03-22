from fastapi import APIRouter, Request, Response

from templates import templates

greet_router = APIRouter()


@greet_router.get("/")
def main_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="main_page.html",
        context={"item_id": 5},
    )


@greet_router.get("/settings")
def settings_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={},
    )
