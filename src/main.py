from fastapi import FastAPI

from routes.game_board import game_board_page
from routes.game_setup import join_game_page, lobby_settings_page, waiting_room_page
from routes.greet import main_page, settings_page
from routes.help import help_page
from routes.auth import auth_router

app = FastAPI()

app.include_router(auth_router)

app.add_route("/game_board", game_board_page, methods=["GET"])

app.add_route("/join_game", join_game_page, methods=["GET"])
app.add_route("/lobby_settings", lobby_settings_page, methods=["GET"])
app.add_route("/waiting_room", waiting_room_page, methods=["GET"])

app.add_route("/", main_page, methods=["GET"])
app.add_route("/settings", settings_page, methods=["GET"])

app.add_route("/help", help_page, methods=["GET"])
