from fastapi import APIRouter, Request, Response

from templates import templates

game_board_router = APIRouter()


@game_board_router.get("/game_board")
def game_board_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={},
    )
