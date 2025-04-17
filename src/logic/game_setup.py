from sqlalchemy.orm import Session

from src.models import GameMode, GameSettings, Lobby


def create_single_player_game(
    session: Session,
    player_nick: str,
    holes_count: int,
    stones_per_hole_count: int,
) -> Lobby:
    settings = GameSettings()
    settings.player_nick = player_nick
    settings.holes_count = holes_count
    settings.stones_per_hole_count = stones_per_hole_count
    settings.game_mode = GameMode.SINGLE_PLAYER
    lobby = Lobby()
    lobby.player1_nick = player_nick
    lobby.player2_nick = None
    lobby.join_code = None
    settings.lobby = lobby
    session.add(settings)
    session.commit()
    return lobby
