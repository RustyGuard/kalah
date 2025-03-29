import uuid

from fastapi import APIRouter, Depends, Request, Response

from routes.auth import auth_required
from templates import templates

game_setup_router = APIRouter(
    dependencies=[
        Depends(auth_required),
    ]
)


@game_setup_router.get("/join_game")
def join_game_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="join_game.html",
        context={},
    )


@game_setup_router.get("/lobby_settings")
def lobby_settings_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="lobby_settings.html",
        context={},
    )


@game_setup_router.get("/waiting_room")
def waiting_room_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="waiting_room.html",
        context={
            "holes_count": 6,
            "stones_count": 1,
            "join_code": uuid.uuid4(),
        },
    )
