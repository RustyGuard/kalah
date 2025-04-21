from typing import Generator

import pytest
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession


@pytest.fixture
def player_socket(
    initialized_multiplayer_board: int,
    player_client: TestClient,
):
    with player_client.websocket_connect(
        f"/ws/{initialized_multiplayer_board}/Player"
    ) as websocket:
        yield websocket


@pytest.fixture
def opponent_socket(
    initialized_multiplayer_board: int,
    opponent_client: TestClient,
) -> Generator[WebSocketTestSession, None, None]:
    with opponent_client.websocket_connect(
        f"/ws/{initialized_multiplayer_board}/Opponent"
    ) as websocket:
        yield websocket


def test_first_turn(
    player_socket: WebSocketTestSession, opponent_socket: WebSocketTestSession
):
    player_socket.send_json(
        {
            "hole": 0,
        }
    )
    assert player_socket.receive_json() == {
        "current_player": "Opponent",
        "holes_player1": [
            0,
            7,
            7,
            7,
            7,
            7,
        ],
        "holes_player2": [
            7,
            6,
            6,
            6,
            6,
            6,
        ],
        "type": "new_state",
    }
    opponent_socket.receive_json()
    opponent_socket.send_json({"hole": 0})
    assert opponent_socket.receive_json() == {
        "current_player": "Player",
        "holes_player1": [
            1,
            8,
            7,
            7,
            7,
            7,
        ],
        "holes_player2": [
            0,
            7,
            7,
            7,
            7,
            7,
        ],
        "type": "new_state",
    }
