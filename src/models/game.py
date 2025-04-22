import enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID as pyUUID

from sqlalchemy import ARRAY, UUID, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import BaseModel

if TYPE_CHECKING:
    from .player import Player


class GameMode(enum.Enum):
    SINGLE_PLAYER = "single_player"
    MULTIPLAYER = "multiplayer"


class Difficulty(enum.Enum):
    EASY = "easy"


class Lobby(BaseModel):
    __tablename__ = "lobby"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player1_nick: Mapped[str] = mapped_column(ForeignKey("player.nickname"))
    player2_nick: Mapped[str | None] = mapped_column(
        ForeignKey("player.nickname"), nullable=True
    )
    join_code: Mapped[pyUUID | None] = mapped_column(UUID)

    # Отношения
    player1: Mapped["Player"] = relationship(foreign_keys=[player1_nick])
    player2: Mapped[Optional["Player"]] = relationship(foreign_keys=[player2_nick])

    # Обратное отношение к GameSettings
    game_settings: Mapped["GameSettings"] = relationship(
        back_populates="lobby", uselist=False
    )


class GameSettings(BaseModel):
    __tablename__ = "game_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    holes_count: Mapped[int] = mapped_column(Integer, nullable=False)
    stones_per_hole_count: Mapped[int] = mapped_column(Integer, nullable=False)
    game_mode: Mapped[GameMode] = mapped_column(Enum(GameMode), nullable=False)
    difficulty_level: Mapped[int]
    lobby_id: Mapped[int] = mapped_column(ForeignKey("lobby.id"))

    # Отношение
    lobby: Mapped["Lobby"] = relationship(back_populates="game_settings")


class GameState(BaseModel):
    __tablename__ = "game_state"

    settings_id: Mapped[int] = mapped_column(
        ForeignKey("game_settings.id"), primary_key=True
    )
    holes_player1: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    holes_player2: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    current_player: Mapped[str | None] = mapped_column(ForeignKey("player.nickname"))

    # Отношения
    settings: Mapped["GameSettings"] = relationship()
    player_turn: Mapped["Player"] = relationship()
