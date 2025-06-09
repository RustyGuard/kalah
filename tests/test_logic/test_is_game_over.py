from src.logic.game_process import is_game_over


def test_player1_win_standard():
    player1 = [0, 0, 0, 0, 0, 0, 25]
    player2 = [0, 0, 0, 0, 0, 0, 20]
    assert is_game_over(player1, player2) is True


def test_player2_win_majority():
    player1 = [0, 0, 0, 0, 0, 0, 20]
    player2 = [0, 0, 0, 0, 0, 0, 21]  # 21 > 20 (всего 41 камень)
    assert is_game_over(player1, player2) is True


def test_draw():
    player1 = [0, 0, 0, 0, 0, 0, 25]
    player2 = [0, 0, 0, 0, 0, 0, 25]
    assert is_game_over(player1, player2) is True


def test_game_continues():
    player1 = [6, 6, 6, 6, 6, 6, 0]
    player2 = [6, 6, 6, 6, 6, 6, 0]
    assert is_game_over(player1, player2) is False
