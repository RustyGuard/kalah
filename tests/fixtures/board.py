import re

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture
def initialized_multiplayer_board(
    player_client: TestClient,
    player_token: str,
    opponent_client: TestClient,
    opponent_token: str,
) -> int:
    response = player_client.post(
        "/lobby_settings",
        data={
            "game_mode": "multi_player",
            "holes_count": "6",
            "stones_count": "6",
            "difficulty_level": "5",
        },
        follow_redirects=False,
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/waiting_room/1"
    response = player_client.get(
        "/waiting_room/1",
        follow_redirects=False,
    )
    assert response.status_code == status.HTTP_200_OK
    join_code = re.search(r"Код приглашения:\s*(.+?)\s*<button", response.text).group(1)  # type: ignore[union-attr]
    with player_client.websocket_connect("/waiting_room/1/ws") as websocket:
        response = opponent_client.post(
            "/join_game",
            data={
                "join_code": join_code,
            },
            follow_redirects=False,
        )
        assert response.status_code == status.HTTP_303_SEE_OTHER
        assert response.headers["location"] == "/game_board/1"
        message = websocket.receive_json()
        assert message == {"event": "Connected"}
    return 1
