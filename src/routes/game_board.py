from fastapi import APIRouter, Request, Response, WebSocket

from templates import templates

game_board_router = APIRouter()


@game_board_router.get("/game_board")
def game_board_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={},
    )


@game_board_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
