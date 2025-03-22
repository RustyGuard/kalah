from fastapi import Request, Response

from templates import templates


def read_root(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="main_page.html",
        context={"item_id": 5},
    )


def settings_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={},
    )
