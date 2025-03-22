from fastapi import Request, Response

from templates import templates


def game_board_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={},
    )
