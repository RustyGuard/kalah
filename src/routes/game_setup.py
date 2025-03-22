from fastapi import Request, Response

from templates import templates


def join_game_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="join_game.html",
        context={},
    )


def lobby_settings_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="lobby_settings.html",
        context={},
    )


def waiting_room_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="waiting_room.html",
        context={},
    )
