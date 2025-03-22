from fastapi import APIRouter, Request, Response

from templates import templates

help_router = APIRouter()


@help_router.get("/help")
def help_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context={},
    )
