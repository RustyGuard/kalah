import pytest

from src.logic.game_process import get_best_turn


@pytest.mark.skip(reason="AI не реализован")
@pytest.mark.parametrize(
    "depth,ai_holes,opponent_holes,expected",
    [
        (3, [6, 6, 6, 6, 6, 6, 0], [6, 6, 6, 6, 6, 6, 0], 1),
        (3, [4, 4, 4, 4, 0], [4, 4, 4, 4, 0], 1),
    ],
)
def test_ai(depth, ai_holes, opponent_holes, expected):
    assert get_best_turn(depth, ai_holes, opponent_holes) == expected
