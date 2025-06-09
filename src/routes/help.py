from fastapi import APIRouter, Depends, Request, Response

from src.routes.auth import auth_required
from src.templates import templates

help_router = APIRouter(
    dependencies=[
        Depends(auth_required),
    ]
)


@help_router.get("/help")
def help_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context={},
    )
