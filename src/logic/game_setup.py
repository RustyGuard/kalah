import uuid
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.models import GameMode, GameSettings, GameState, Lobby


def create_game_state(settings: GameSettings) -> GameState:
    state = GameState()
    state.settings = settings
    state.holes_player1 = [settings.stones_per_hole_count] * (settings.holes_count - 1) + [0]
    state.holes_player2 = [settings.stones_per_hole_count] * (settings.holes_count - 1) + [0]
    state.current_player = settings.lobby.player1_nick
    return state


def create_single_player_game(
    session: Session,
    player_nick: str,
    holes_count: int,
    stones_per_hole_count: int,
    difficulty_level: int,
) -> GameSettings:
    settings = GameSettings()
    settings.holes_count = holes_count
    settings.stones_per_hole_count = stones_per_hole_count
    settings.game_mode = GameMode.SINGLE_PLAYER
    settings.difficulty_level = difficulty_level
    lobby = Lobby()
    lobby.player1_nick = player_nick
    lobby.player2_nick = None
    lobby.join_code = None
    settings.lobby = lobby
    session.add(settings)
    state = create_game_state(settings)
    session.add(state)
    session.commit()
    return settings


def create_multiplayer_game(
    session: Session,
    player_nick: str,
    holes_count: int,
    stones_per_hole_count: int,
) -> GameSettings:
    settings = GameSettings()
    settings.holes_count = holes_count
    settings.stones_per_hole_count = stones_per_hole_count
    settings.game_mode = GameMode.MULTIPLAYER
    settings.difficulty_level = 3
    lobby = Lobby()
    lobby.player1_nick = player_nick
    lobby.player2_nick = None
    lobby.join_code = uuid.uuid4()
    settings.lobby = lobby
    session.add(settings)
    session.commit()
    return settings


def join_player(
    session: Session,
    join_code: str,
    opponent_nick: str,
) -> GameSettings:
    lobby: Lobby | None = session.scalar(
        select(Lobby).where(Lobby.join_code == UUID(join_code))
    )
    assert lobby is not None
    settings = lobby.game_settings
    settings.lobby.player2_nick = opponent_nick
    settings.lobby.join_code = None
    state = create_game_state(settings)
    session.add(state)
    session.add(settings.lobby)
    session.commit()
    return settings
