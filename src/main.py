from fastapi import FastAPI

from routes.auth import auth_router
from routes.game_board import game_board_router
from routes.game_setup import game_setup_router
from routes.greet import greet_router
from routes.help import help_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(game_board_router)
app.include_router(game_setup_router)
app.include_router(greet_router)
app.include_router(help_router)
