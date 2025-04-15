import asyncio
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response, WebSocket, status
from fastapi.responses import RedirectResponse

from src.routes.auth import auth_required
from src.templates import templates

game_setup_router = APIRouter()


@game_setup_router.get("/join_game")
def join_game_page(request: Request, _=Depends(auth_required)) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="join_game.html",
        context={},
    )


@game_setup_router.post("/join_game")
def join_game(join_code: Annotated[str, Form()], _=Depends(auth_required)):
    return RedirectResponse("/game_board", status_code=status.HTTP_303_SEE_OTHER)


@game_setup_router.get("/lobby_settings")
def lobby_settings_page(request: Request, _=Depends(auth_required)) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="lobby_settings.html",
        context={},
    )


@game_setup_router.post("/lobby_settings")
def lobby_settings(
    game_mode: Annotated[str, Form()],
    holes_count: Annotated[str, Form()],
    stones_count: Annotated[str, Form()],
    difficulty_level: Annotated[str, Form()],
    _=Depends(auth_required),
):
    if game_mode == "single_player":
        return RedirectResponse("/game_board", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/waiting_room", status_code=status.HTTP_303_SEE_OTHER)


@game_setup_router.get("/waiting_room")
def waiting_room_page(request: Request, _=Depends(auth_required)) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="waiting_room.html",
        context={
            "holes_count": 6,
            "stones_count": 1,
            "join_code": uuid.uuid4(),
        },
    )


@game_setup_router.websocket("/waiting_room/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(10.0)
        await websocket.send_text("Connected")
