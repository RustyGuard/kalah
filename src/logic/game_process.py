import itertools


def make_a_turn(
    current_player_holes: list[int], opponent_holes: list[int], selected_cell_index: int
) -> bool:
    """
    Совершаем ход и возвращаем, остается ли ход у игрока
    """

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

        # Пропускаем калах оппонента
        if (
            current_side_index == 1
            and current_cell_index == len(sides[current_side_index]) - 1
        ):
            current_cell_index = 0
            current_side_index = 0

        sides[current_side_index][current_cell_index] += 1
        stones_to_distribute -= 1

    # Правило захвата
    if (
        current_side_index == 0
        and current_cell_index != len(sides[current_side_index]) - 1
        and sides[current_side_index][current_cell_index] == 1
        and sides[1 - current_side_index][-(current_cell_index + 2)] > 0
    ):
        sides[current_side_index][-1] += sides[current_side_index][current_cell_index]
        sides[current_side_index][-1] += sides[1 - current_side_index][
            -(current_cell_index + 2)
        ]
        sides[current_side_index][current_cell_index] = 0
        sides[1 - current_side_index][-(current_cell_index + 2)] = 0

    if (
        current_side_index == 0
        and current_cell_index == len(sides[current_side_index]) - 1
    ):
        return True

    return False


def can_turn_be_made(current_player_holes: list[int]) -> bool:
    return any(current_player_holes[:-1])


def is_game_over(player1_holes: list[int], player2_holes: list[int]) -> bool:
    stones_count = sum(itertools.chain(player1_holes, player2_holes))
    if player1_holes[-1] > stones_count // 2:
        return True
    if player2_holes[-1] > stones_count // 2:
        return True
    # Проверяем, пусты ли все лунки игрока (кроме калаха)
    if all(count == 0 for count in player1_holes[:-1]):
        return True
    # Проверяем, пусты ли все лунки противника (кроме калаха)
    if all(count == 0 for count in player2_holes[:-1]):
        return True
    return False


def finish_game(player1_holes: list[int], player2_holes: list[int]):
    """
    Завершает игру, перемещая все оставшиеся камни в калахи соответствующих игроков.
    """

    # Собираем камни игрока ИИ
    player1_holes[-1] += sum(player1_holes[:-1])
    for i in range(len(player1_holes) - 1):
        player1_holes[i] = 0

    # Собираем камни противника
    player2_holes[-1] += sum(player2_holes[:-1])
    for i in range(len(player2_holes) - 1):
        player2_holes[i] = 0


def get_game_over_message(
    player1_holes: list[int],
    player2_holes: list[int],
    player1_nick: str,
    player2_nick: str,
) -> str:
    if player1_holes[-1] > player2_holes[-1]:
        return f"Победил {player1_nick}!"
    elif player2_holes[-1] > player1_holes[-1]:
        return f"Победил {player2_nick}!"
    else:
        return "Ничья!"


class KalahAI:
    """
    Класс для искусственного интеллекта в игре калах.
    Использует алгоритм минимакс с альфа-бета отсечением для поиска лучшего хода.
    """

    @staticmethod
    def evaluate_board(ai_holes: list[int], opponent_holes: list[int]) -> int:
        """
        Оценивает текущее состояние доски с точки зрения ИИ.
        Возвращает положительное значение, если состояние благоприятно для ИИ.
        """
        # Основная оценка - разница между калахами
        kalah_diff = ai_holes[-1] - opponent_holes[-1]

        # Учитываем также количество камней в обычных лунках
        ai_stones = sum(ai_holes[:-1])
        opponent_stones = sum(opponent_holes[:-1])

        # Предпочитаем держать камни в своих лунках
        position_value = (ai_stones - opponent_stones) // 2

        return kalah_diff * 3 + position_value

    @staticmethod
    def get_valid_moves(holes: list[int]) -> list[int]:
        """
        Возвращает список индексов лунок, из которых можно сделать ход.
        """
        return [i for i in range(len(holes) - 1) if holes[i] > 0]

    @staticmethod
    def simulate_move(
        current_holes: list[int], opponent_holes: list[int], move_index: int
    ) -> tuple[list[int], list[int], bool]:
        """
        Симулирует ход и возвращает новое состояние доски и флаг,
        показывающий, получает ли игрок дополнительный ход.
        """
        # Создаем копии для симуляции
        current = current_holes.copy()
        opponent = opponent_holes.copy()

        # Симулируем ход, используя make_a_turn
        extra_turn = make_a_turn(current, opponent, move_index)

        return current, opponent, extra_turn

    @staticmethod
    def simulate_finish_game(
        ai_holes: list[int], opponent_holes: list[int]
    ) -> tuple[list[int], list[int]]:
        """
        Симулирует завершение игры, перемещая все оставшиеся камни в калахи
        соответствующих игроков. Возвращает новое состояние доски.
        """
        final_ai = ai_holes.copy()
        final_opponent = opponent_holes.copy()

        finish_game(final_ai, final_opponent)

        return final_ai, final_opponent

    def minimax(
        self,
        depth: int,
        ai_holes: list[int],
        opponent_holes: list[int],
        is_ai_turn: bool,
        alpha: int | float = float("-inf"),
        beta: int | float = float("inf"),
    ) -> tuple[int | float, int | None]:
        """
        Алгоритм минимакс с альфа-бета отсечением для нахождения лучшего хода.
        Возвращает (оценка, лучший_ход). Если глубина = 0 или игра закончена, возвращает (оценка, None).
        """
        if depth == 0 or is_game_over(ai_holes, opponent_holes):
            return self.evaluate_board(ai_holes, opponent_holes), None

        if is_game_over(ai_holes, opponent_holes):
            final_ai, final_opponent = self.simulate_finish_game(
                ai_holes, opponent_holes
            )
            return self.evaluate_board(final_ai, final_opponent), None

        if is_ai_turn:
            # Максимизирующий игрок (ИИ)
            best_value = float("-inf")
            best_move = None

            # Перебираем все возможные ходы
            for move in self.get_valid_moves(ai_holes):
                # Симулируем ход
                new_ai, new_opponent, extra_turn = self.simulate_move(
                    ai_holes, opponent_holes, move
                )

                # Рекурсивный вызов (с тем же игроком, если есть дополнительный ход)
                value, _ = self.minimax(
                    depth - 1, new_ai, new_opponent, extra_turn, alpha, beta
                )

                # Обновляем лучший ход
                if value > best_value:
                    best_value = value
                    best_move = move

                # Альфа-бета отсечение
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            return best_value, best_move
        else:
            # Минимизирующий игрок (противник)
            best_value = float("inf")
            best_move = None

            # Перебираем все возможные ходы
            for move in self.get_valid_moves(opponent_holes):
                # Симулируем ход (меняем местами противника и ИИ)
                new_opponent, new_ai, extra_turn = self.simulate_move(
                    opponent_holes, ai_holes, move
                )

                # Рекурсивный вызов (с тем же игроком, если есть дополнительный ход)
                value, _ = self.minimax(
                    depth - 1, new_ai, new_opponent, not extra_turn, alpha, beta
                )

                # Обновляем лучший ход
                if value < best_value:
                    best_value = value
                    best_move = move

                # Альфа-бета отсечение
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

            return best_value, best_move

    def get_best_turn(
        self, depth: int, ai_holes: list[int], opponent_holes: list[int]
    ) -> int | None:
        """
        Возвращает индекс лучшей лунки для хода ИИ.
        Если нет возможных ходов, возвращает None.

        Параметры:
        - depth: глубина просчета (сколько ходов вперед анализировать)
        - ai_holes: список лунок ИИ (последняя лунка - калах)
        - opponent_holes: список лунок противника (последняя лунка - калах)
        """
        valid_moves = self.get_valid_moves(ai_holes)

        # Если нет возможных ходов, возвращаем None
        if not valid_moves:
            return None

        # Запускаем минимакс для поиска лучшего хода
        _, best_move = self.minimax(depth, ai_holes, opponent_holes, True)

        return best_move


# Функция-обертка для сохранения предыдущей сигнатуры
def get_best_turn(
    depth: int, ai_holes: list[int], opponent_holes: list[int]
) -> int | None:
    """
    Возвращает индекс лучшей лунки для хода ИИ.
    Если нет возможных ходов, возвращает None.

    Параметры:
    - depth: глубина просчета (сколько ходов вперед анализировать)
    - ai_holes: список лунок ИИ (последняя лунка - калах)
    - opponent_holes: список лунок противника (последняя лунка - калах)
    """
    ai = KalahAI()
    return ai.get_best_turn(depth, ai_holes, opponent_holes)
