import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "page_path",
    [
        "/",
        "/settings",
        "/help",
        "/join_game",
        "/lobby_settings",
        "/waiting_room",
        "/game_board",
    ],
)
def test_auth_redirect(test_client: TestClient, page_path: str):
    response = test_client.get(page_path, follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
