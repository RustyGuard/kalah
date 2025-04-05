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
def test_auth_redirect(player_client: TestClient, page_path: str):
    """Not authorized users should be redirected to `/auth` page"""
    response = player_client.get(page_path, follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT


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
def test_get_with_cookie(player_client: TestClient, player_token: str, page_path: str):
    """Authorized users should be able to access pages"""
    assert isinstance(player_token, str)
    response = player_client.get(page_path, follow_redirects=False)
    assert response.status_code == status.HTTP_200_OK
