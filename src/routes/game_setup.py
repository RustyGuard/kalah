import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response, WebSocket, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.database import get_session
from src.logic.game_setup import (
    create_multiplayer_game,
    create_single_player_game,
    join_player,
)
from src.models import GameSettings
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
def join_game(
    session: Annotated[Session, Depends(get_session)],
    join_code: Annotated[str, Form()],
    player=Depends(auth_required),
):
    settings = join_player(
        session,
        join_code,
        player["user_name"],
    )
    return RedirectResponse(
        f"/game_board/{settings.id}", status_code=status.HTTP_303_SEE_OTHER
    )


@game_setup_router.get("/lobby_settings")
def lobby_settings_page(request: Request, _=Depends(auth_required)) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="lobby_settings.html",
        context={},
    )


@game_setup_router.post("/lobby_settings")
def lobby_settings(
    session: Annotated[Session, Depends(get_session)],
    game_mode: Annotated[str, Form()],
    holes_count: Annotated[str, Form()],
    stones_count: Annotated[str, Form()],
    difficulty_level: Annotated[str, Form()],  # todo
    player=Depends(auth_required),
):
    if game_mode == "single_player":
        settings = create_single_player_game(
            session,
            player_nick=player["user_name"],
            holes_count=int(holes_count),
            stones_per_hole_count=int(stones_count),
            difficulty_level=int(difficulty_level),
        )
        return RedirectResponse(
            f"/game_board/{settings.id}", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        settings = create_multiplayer_game(
            session,
            player_nick=player["user_name"],
            holes_count=int(holes_count),
            stones_per_hole_count=int(stones_count),
        )
        return RedirectResponse(
            f"/waiting_room/{settings.id}", status_code=status.HTTP_303_SEE_OTHER
        )


@game_setup_router.get("/waiting_room/{settings_id}")
def waiting_room_page(
    session: Annotated[Session, Depends(get_session)],
    request: Request,
    settings_id: int,
    _=Depends(auth_required),
) -> Response:
    settings: GameSettings | None = session.scalar(
        select(GameSettings).where(GameSettings.id == settings_id)
    )
    assert settings is not None
    return templates.TemplateResponse(
        request=request,
        name="waiting_room.html",
        context={
            "holes_count": settings.holes_count,
            "stones_count": settings.stones_per_hole_count,
            "join_code": settings.lobby.join_code,
            "settings_id": settings_id,
        },
    )


@game_setup_router.websocket("/waiting_room/{settings_id}/ws")
async def websocket_endpoint(
    session: Annotated[Session, Depends(get_session)],
    websocket: WebSocket,
    settings_id: int,
):
    settings: GameSettings | None = session.scalar(
        select(GameSettings).where(GameSettings.id == settings_id)
    )
    assert settings is not None
    await websocket.accept()
    while True:
        await asyncio.sleep(1.0)
        session.refresh(settings)
        if settings.lobby.player2_nick is not None:
            await websocket.send_json({"event": "Connected"})
