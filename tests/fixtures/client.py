import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.app import get_application


@pytest.fixture
def test_app():
    return get_application()


@pytest.fixture
def player_client(test_app):
    yield TestClient(test_app)


@pytest.fixture
def player_token(player_client):
    response = player_client.post(
        "/auth",
        data={
            "user_name": "Player",
            "avatar_id": 1,
        },
        follow_redirects=False,
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    return response.cookies["access_token"]


@pytest.fixture
def opponent_client(test_app):
    yield TestClient(test_app)


@pytest.fixture
def opponent_token(opponent_client):
    response = opponent_client.post(
        "/auth",
        data={
            "user_name": "Opponent",
            "avatar_id": 2,
        },
        follow_redirects=False,
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    return response.cookies["access_token"]
