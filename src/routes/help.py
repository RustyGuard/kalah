from fastapi import Request, Response

from templates import templates


def help_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="help.html",
        context={},
    )
