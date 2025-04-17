from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, WebSocket
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.database import get_session
from src.models import GameState
from src.routes.auth import auth_required
from src.templates import templates

game_board_router = APIRouter()


@game_board_router.get("/game_board/{settings_id}")
def game_board_page(
    session: Annotated[Session, Depends(get_session)],
    request: Request,
    settings_id: int,
    _=Depends(auth_required),
) -> Response:
    state: GameState | None = session.scalar(
        select(GameState).where(GameState.settings_id == settings_id)
    )
    assert state is not None
    print(f"{state.settings.lobby.player2_nick=}")
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={},
    )


@game_board_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
