import asyncio
from collections import defaultdict
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, WebSocket
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import select

from src.database import get_session
from src.logic.game_process import (
    can_turn_be_made,
    finish_game,
    get_best_turn,
    get_game_over_message,
    is_game_over,
    make_a_turn,
)
from src.models import GameMode, GameState
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
    current_player_name = player["user_name"]
    current_player_avatar = request.url_for(
        "static", path=f"images/avatars/avatar{player['avatar_id']}.svg"
    )
    if state.settings.lobby.player1_nick == current_player_name:
        current_player_holes = state.holes_player1
        current_player_key = "holes_player1"
        opponent_player_holes = state.holes_player2
        opponent_player_key = "holes_player2"
        if state.settings.lobby.player2_nick is not None:
            assert state.settings.lobby.player2 is not None
            opponent_player_avatar = request.url_for(
                "static",
                path=f"images/avatars/avatar{state.settings.lobby.player2.avatar_id}.svg",
            )
        else:
            opponent_player_avatar = request.url_for(
                "static", path="images/avatars/bot.svg"
            )
        opponent_player_name = state.settings.lobby.player2_nick or "Bot"
    else:
        current_player_holes = state.holes_player2
        current_player_key = "holes_player2"
        opponent_player_holes = state.holes_player1
        opponent_player_key = "holes_player1"
        opponent_player_avatar = request.url_for(
            "static",
            path=f"images/avatars/avatar{state.settings.lobby.player1.avatar_id}.svg",
        )
        opponent_player_name = state.settings.lobby.player1_nick

    print(f"{state.settings.lobby.player2_nick=}")
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={
            "state": state,
            "settings_id": settings_id,
            "current_player_name": current_player_name,
            "opponent_player_name": opponent_player_name,
            "current_player_avatar": current_player_avatar,
            "opponent_player_avatar": opponent_player_avatar,
            "current_player_holes": current_player_holes,
            "current_player_key": current_player_key,
            "opponent_player_holes": opponent_player_holes,
            "opponent_player_key": opponent_player_key,
        },
    )


async def handle_single_player(
    session: Session,
    websocket: WebSocket,
    state: GameState,
    player_nick: str,
):
    while not is_game_over(state.holes_player1, state.holes_player2):
        if state.current_player == state.settings.lobby.player1_nick:
            if can_turn_be_made(state.holes_player1):
                data = await websocket.receive_json()
                bonus_turn = make_a_turn(
                    state.holes_player1, state.holes_player2, int(data["hole"])
                )
                flag_modified(state, "holes_player1")
                flag_modified(state, "holes_player2")
                if not bonus_turn:
                    state.current_player = None
            else:
                state.current_player = None
        else:
            if can_turn_be_made(state.holes_player2):
                await asyncio.sleep(1.0)
                ai_turn = get_best_turn(
                    state.settings.difficulty_level,
                    state.holes_player2,
                    state.holes_player1,
                )
                print(ai_turn)
                assert ai_turn is not None
                bonus_turn = make_a_turn(
                    state.holes_player2, state.holes_player1, ai_turn
                )
                flag_modified(state, "holes_player1")
                flag_modified(state, "holes_player2")
                if not bonus_turn:
                    state.current_player = player_nick
            else:
                state.current_player = player_nick
        session.commit()
        await websocket.send_json(
            {
                "type": "new_state",
                "holes_player1": state.holes_player1,
                "holes_player2": state.holes_player2,
                "current_player": state.current_player,
            }
        )
    finish_game(state.holes_player1, state.holes_player2)
    await websocket.send_json(
        {
            "type": "new_state",
            "holes_player1": state.holes_player1,
            "holes_player2": state.holes_player2,
            "current_player": state.current_player,
        }
    )
    await websocket.send_json(
        {
            "type": "game_over",
            "message": get_game_over_message(
                state.holes_player1,
                state.holes_player2,
                state.settings.lobby.player1_nick,
                "Bot",
            ),
        }
    )


settings_id_to_sockets: defaultdict[int, list[WebSocket]] = defaultdict(list)


async def handle_multiplayer(
    session: Session,
    websocket: WebSocket,
    state: GameState,
    player_nick: str,
):
    settings_id_to_sockets[state.settings_id].append(websocket)
    while True:
        data = await websocket.receive_json()
        session.refresh(state)
        if state.settings.lobby.player1_nick == player_nick:
            bonus_turn = make_a_turn(
                state.holes_player1, state.holes_player2, int(data["hole"])
            )
            if can_turn_be_made(state.holes_player2) and not bonus_turn:
                state.current_player = state.settings.lobby.player2_nick
        else:
            bonus_turn = make_a_turn(
                state.holes_player2, state.holes_player1, int(data["hole"])
            )
            if can_turn_be_made(state.holes_player1) and not bonus_turn:
                state.current_player = state.settings.lobby.player1_nick
        print(
            f"{state.current_player=} {state.settings.lobby.player1_nick=} {state.settings.lobby.player2_nick=}"
        )
        flag_modified(state, "holes_player1")
        flag_modified(state, "holes_player2")
        session.commit()
        for player_socket in settings_id_to_sockets[state.settings_id].copy():
            try:
                await player_socket.send_json(
                    {
                        "type": "new_state",
                        "holes_player1": state.holes_player1,
                        "holes_player2": state.holes_player2,
                        "current_player": state.current_player,
                    }
                )
            except RuntimeError:
                settings_id_to_sockets[state.settings_id].remove(player_socket)
        if is_game_over(state.holes_player1, state.holes_player2):
            finish_game(state.holes_player1, state.holes_player2)
            for player_socket in settings_id_to_sockets[state.settings_id].copy():
                try:
                    await player_socket.send_json(
                        {
                            "type": "new_state",
                            "holes_player1": state.holes_player1,
                            "holes_player2": state.holes_player2,
                            "current_player": state.current_player,
                        }
                    )
                    await player_socket.send_json(
                        {
                            "type": "game_over",
                            "message": get_game_over_message(
                                state.holes_player1,
                                state.holes_player2,
                                state.settings.lobby.player1_nick,
                                state.settings.lobby.player2_nick,  # type: ignore[arg-type]
                            ),
                        }
                    )
                except RuntimeError:
                    settings_id_to_sockets[state.settings_id].remove(player_socket)
            break


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
    try:
        if state.settings.game_mode == GameMode.SINGLE_PLAYER:
            await handle_single_player(session, websocket, state, player_nick)
        else:
            await handle_multiplayer(session, websocket, state, player_nick)
    except WebSocketDisconnect:
        pass
