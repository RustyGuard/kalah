from fastapi import FastAPI

from routes.auth import authorize_page, authorize_user
from routes.game_board import game_board_page
from routes.game_setup import join_game_page, lobby_settings_page, waiting_room_page
from routes.greet import read_root, settings_page
from routes.help import help_page

app = FastAPI()

app.add_route("/auth", authorize_page, methods=["GET"])
app.add_route("/auth", authorize_user, methods=["POST"])  # type: ignore[arg-type]

app.add_route("/game_board", game_board_page, methods=["GET"])

app.add_route("/join_game", join_game_page, methods=["GET"])
app.add_route("/lobby_settings", lobby_settings_page, methods=["GET"])
app.add_route("/waiting_room", waiting_room_page, methods=["GET"])

app.add_route("/", read_root, methods=["GET"])
app.add_route("/settings", settings_page, methods=["GET"])

app.add_route("/help", help_page, methods=["GET"])
