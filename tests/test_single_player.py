from fastapi import status
from fastapi.testclient import TestClient


def test_create_single_player_game(player_client: TestClient, player_token: str):
    response = player_client.post(
        "/lobby_settings",
        data={
            "game_mode": "single_player",
            "holes_count": "6",
            "stones_count": "6",
            "difficulty_level": "5",
        },
        follow_redirects=False,
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/game_board/1"
    response = player_client.get(
        "/game_board/1",
    )
    assert response.status_code == status.HTTP_200_OK
