from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from routes.auth import AuthError, auth_router
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

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(AuthError)
def exception_handler(request: Request, error: AuthError):
    return RedirectResponse("/auth")
