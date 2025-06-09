from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel


class Player(BaseModel):
    __tablename__ = "player"

    nickname: Mapped[str] = mapped_column(String, primary_key=True)
    avatar_id: Mapped[int] = mapped_column(Integer)
