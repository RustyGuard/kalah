import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from core.config import settings
from routes.auth import AuthError


def get_application() -> FastAPI:
    docs = (
        {"docs_url": None, "redoc_url": None, "openapi_url": None}
        if not settings.DEBUG
        else {}
    )
    _app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, **docs)  # type: ignore[arg-type]

    init_extensions(_app)
    init_middlewares(_app)
    init_routers(_app)
    init_errors_handlers(_app)

    return _app


def init_extensions(app: FastAPI) -> None:
    # init the logger as usual
    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    )


def init_routers(app: FastAPI) -> None:
    from routes.auth import auth_router
    from routes.game_board import game_board_router
    from routes.game_setup import game_setup_router
    from routes.greet import greet_router
    from routes.help import help_router

    @app.get("/ping")
    async def ping() -> dict[str, bool | str]:
        return {"ok": True, "detail": "pong"}

    app.include_router(auth_router)
    app.include_router(game_board_router)
    app.include_router(game_setup_router)
    app.include_router(greet_router)
    app.include_router(help_router)

    app.mount("/static", StaticFiles(directory="static"), name="static")


def init_errors_handlers(app: FastAPI) -> None:
    from exceptions_handlers import unauthorized_handler

    # ToDo глянуть валидно ли
    app.add_exception_handler(AuthError, unauthorized_handler)  # type: ignore[arg-type]
