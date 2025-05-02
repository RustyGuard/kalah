import itertools
import random


def make_a_turn(
    current_player_holes: list[int], opponent_holes: list[int], selected_cell_index: int
) -> None:
    stones_to_distribute = current_player_holes[selected_cell_index]
    sides = [current_player_holes, opponent_holes]
    current_player_holes[selected_cell_index] = 0
    current_cell_index = selected_cell_index
    current_side_index = 0
    while stones_to_distribute:
        current_cell_index += 1
        if current_cell_index >= len(sides[current_side_index]):
            current_cell_index = 0
            current_side_index = 1 - current_side_index
        sides[current_side_index][current_cell_index] += 1
        stones_to_distribute -= 1


def get_best_turn(ai_holes: list[int], opponent_holes: list[int]) -> int | None:
    try:
        return random.choice(
            [(i, hole) for i, hole in enumerate(ai_holes[:-1]) if hole]
        )[0]
    except IndexError:
        return None


def can_turn_be_made(current_player_holes: list[int]) -> bool:
    return any(current_player_holes[:-1])


def is_game_over(player1_holes: list[int], player2_holes: list[int]) -> bool:
    stones_count = sum(itertools.chain(player1_holes, player2_holes))
    if player1_holes[-1] > stones_count // 2:
        return True
    if player2_holes[-1] > stones_count // 2:
        return True
    if not any(itertools.chain(player1_holes[:-1], player2_holes[:-1])):
        return True
    return False
