import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, WebSocket
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import select

from src.database import get_session
from src.logic.game_process import get_best_turn, make_a_turn
from src.models import GameState
from src.routes.auth import auth_required
from src.templates import templates

game_board_router = APIRouter()


@game_board_router.get("/game_board/{settings_id}")
def game_board_page(
    session: Annotated[Session, Depends(get_session)],
    request: Request,
    settings_id: int,
    player=Depends(auth_required),
) -> Response:
    state: GameState | None = session.scalar(
        select(GameState).where(GameState.settings_id == settings_id)
    )
    assert state is not None
    print(f"{state.settings.lobby.player2_nick=}")
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={
            "state": state,
            "settings_id": settings_id,
            "current_player": player,
            "current_player_avatar": request.url_for(
                "static", path=f"images/avatars/avatar{player['avatar_id']}.svg"
            ),
        },
    )


@game_board_router.websocket("/ws/{settings_id}/{player_nick}")
async def websocket_endpoint(
    session: Annotated[Session, Depends(get_session)],
    websocket: WebSocket,
    settings_id: int,
    player_nick: str,
):
    state: GameState | None = session.scalar(
        select(GameState).where(GameState.settings_id == settings_id)
    )
    assert state is not None
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        make_a_turn(state.holes_player1, state.holes_player2, int(data["hole"]))
        flag_modified(state, "holes_player1")
        flag_modified(state, "holes_player2")
        state.current_player = None
        session.commit()
        print(data)
        await websocket.send_json(
            {
                "type": "new_state",
                "holes_player1": state.holes_player1,
                "holes_player2": state.holes_player2,
                "current_player": state.current_player,
            }
        )
        await asyncio.sleep(1.0)
        ai_turn = get_best_turn(state.holes_player2, state.holes_player1)
        make_a_turn(state.holes_player2, state.holes_player1, ai_turn)
        flag_modified(state, "holes_player1")
        flag_modified(state, "holes_player2")
        state.current_player = player_nick
        session.commit()
        print(data)
        await websocket.send_json(
            {
                "type": "new_state",
                "holes_player1": state.holes_player1,
                "holes_player2": state.holes_player2,
                "current_player": state.current_player,
            }
        )
