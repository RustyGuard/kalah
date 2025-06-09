from src.logic.game_process import make_a_turn


def test_basic_move():
    """Test a basic move without extra turn or capture."""
    current_player = [4, 4, 4, 4, 4, 4, 0]  # Last element is the kalah
    opponent = [4, 4, 4, 4, 4, 4, 0]  # Last element is the kalah

    # Select the first pit (index 0)
    extra_turn = make_a_turn(current_player, opponent, 0)

    # Expected state after move:
    # - Current player's pit at index 0 should be empty
    # - Stones should be distributed in subsequent pits
    expected_current_player = [0, 5, 5, 5, 5, 4, 0]
    expected_opponent = [4, 4, 4, 4, 4, 4, 0]

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False


def test_extra_turn():
    """Test a move that ends in the player's kalah, granting an extra turn."""
    current_player = [0, 0, 0, 0, 0, 1, 0]  # Only 1 stone in last pit
    opponent = [4, 4, 4, 4, 4, 4, 0]

    # Select the pit with 1 stone (index 5) - should end in kalah
    extra_turn = make_a_turn(current_player, opponent, 5)

    expected_current_player = [0, 0, 0, 0, 0, 0, 1]  # Stone moved to kalah
    expected_opponent = [4, 4, 4, 4, 4, 4, 0]  # No change

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is True  # Last stone in own kalah = extra turn


def test_capture_rule():
    """Test the capture rule when landing in an empty pit."""
    current_player = [0, 0, 0, 0, 1, 0, 0]
    opponent = [5, 5, 5, 5, 5, 5, 0]

    # Moving the single stone to an empty pit should trigger capture
    extra_turn = make_a_turn(current_player, opponent, 4)

    # Stone lands in pit 5, which was empty, should capture
    # The opponent's corresponding pit is determined by: -(current_cell_index + 2)
    # For pit 5, that's equivalent to index 0 in the opponent array
    expected_current_player = [0, 0, 0, 0, 0, 0, 6]  # 1 from landing + 5 captured
    expected_opponent = [0, 5, 5, 5, 5, 5, 0]

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False


def test_long_move_across_both_sides():
    """Test a move with many stones that wraps around both sides."""
    current_player = [0, 0, 0, 0, 0, 12, 0]
    opponent = [4, 4, 4, 4, 4, 4, 0]

    # Moving 12 stones from index 5
    extra_turn = make_a_turn(current_player, opponent, 5)

    # Tracing the distribution with the skip opponent's kalah rule:
    # - Stones: 12
    # - 1 stone to current[6] (kalah) -> 11 stones left
    # - 6 stones to opponent[0-5] -> 5 stones left
    # - 5 stones to current[0-4]
    # - Last stone lands in current[4], which was empty (0->1)
    # - This triggers capture rule, capturing opponent[1]

    # After initial distribution:
    # current = [1, 1, 1, 1, 1, 0, 1]
    # opponent = [5, 5, 5, 5, 5, 5, 0]

    # After capture rule:
    # - current[4] (1) gets captured into kalah
    # - opponent[1] (5) gets captured into current's kalah
    expected_current_player = [1, 1, 1, 1, 0, 0, 7]  # 1 + 1 + 5 in kalah
    expected_opponent = [5, 0, 5, 5, 5, 5, 0]  # opponent[1] emptied

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False


def test_no_capture_on_kalah():
    """Test that captures don't occur when landing in the kalah."""
    current_player = [0, 0, 0, 0, 0, 1, 0]
    opponent = [4, 4, 4, 4, 4, 4, 0]

    extra_turn = make_a_turn(current_player, opponent, 5)

    expected_current_player = [0, 0, 0, 0, 0, 0, 1]
    expected_opponent = [4, 4, 4, 4, 4, 4, 0]

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is True  # Extra turn for ending in kalah


def test_no_capture_when_landing_with_existing_stones():
    """Test that capture doesn't occur when landing in a pit that already had stones."""
    current_player = [0, 0, 0, 2, 1, 5, 0]
    opponent = [5, 5, 5, 5, 5, 5, 0]

    # Moving from index 4 to index 5, which already has stones
    extra_turn = make_a_turn(current_player, opponent, 4)

    expected_current_player = [0, 0, 0, 2, 0, 6, 0]
    expected_opponent = [5, 5, 5, 5, 5, 5, 0]

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False


def test_capture_calculation():
    """Test the exact calculation for capture from the opposite side."""
    current_player = [0, 0, 3, 0, 0, 0, 0]
    opponent = [0, 0, 0, 7, 0, 0, 0]

    # Moving 3 stones from index 2 will land in empty pit 5
    # This should trigger capture from opponent's corresponding pit (index 2)
    extra_turn = make_a_turn(current_player, opponent, 2)

    expected_current_player = [0, 0, 0, 1, 1, 1, 0]
    expected_opponent = [0, 0, 0, 7, 0, 0, 0]

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False


def test_skip_opponent_kalah():
    """Test that distribution skips the opponent's kalah."""
    current_player = [1, 1, 1, 1, 1, 2, 0]  # Only 2 stones to distribute
    opponent = [1, 1, 1, 1, 1, 1, 5]  # Opponent's kalah has 5 stones

    # Moving 2 stones from index 5
    # First stone goes to own kalah, second stone should go to first opponent pit
    # skipping the opponent's kalah
    extra_turn = make_a_turn(current_player, opponent, 5)

    expected_current_player = [1, 1, 1, 1, 1, 0, 1]  # First stone in kalah
    expected_opponent = [
        2,
        1,
        1,
        1,
        1,
        1,
        5,
    ]  # Second stone in first pit, kalah unchanged

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False


def test_empty_pit_selection():
    """Test selecting an empty pit (which should be invalid in the real game)."""
    current_player = [4, 0, 4, 4, 4, 4, 0]
    opponent = [4, 4, 4, 4, 4, 4, 0]

    # Selecting empty pit at index 1
    extra_turn = make_a_turn(current_player, opponent, 1)

    # No stones to move, so board should remain unchanged
    expected_current_player = [4, 0, 4, 4, 4, 4, 0]
    expected_opponent = [4, 4, 4, 4, 4, 4, 0]

    assert current_player == expected_current_player
    assert opponent == expected_opponent
    assert extra_turn is False  # No extra turn
