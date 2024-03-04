import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(4, 2021)


def main():
    lines = advent.get_input_lines()
    draws = [int(i) for i in lines[0].split(",")]
    boards = get_boards(lines[2:])

    draw, board = first_winner(draws, boards)
    total = draw * board[board != -1].sum()
    advent.submit(1, total)

    draw, board = last_winner(draws, boards)
    total = draw * board[board != -1].sum()
    advent.submit(2, total)


def last_winner(
    draws: list[int], boards: list[npt.NDArray[np.int_]]
) -> tuple[int, npt.NDArray[np.bool_]]:
    won: set[int] = set()
    ids = set(range(len(boards)))
    for d in draws:
        for id in ids - won:
            board = boards[id]
            board[board == d] = -1
            if is_winner(board):
                won.add(id)
            if len(won) == len(boards):
                return d, boards[id]

    return draws[-1], boards[-1]


def first_winner(  # type: ignore
    draws: list[int], boards: list[npt.NDArray[np.int_]]
) -> tuple[int, npt.NDArray[np.bool_]]:
    for d in draws:
        for board in boards:
            board[board == d] = -1
            if is_winner(board):
                return d, board

    return -1, boards[0]


def is_winner(board: npt.NDArray[np.int_]) -> bool:
    return (board.sum(axis=0) == -5).any() or (board.sum(axis=1) == -5).any()


def get_boards(lines: list[str]) -> list[npt.NDArray[np.int_]]:
    board = []
    boards = []
    for line in lines:
        if line != "":
            board.append([int(i) for i in line.split()])
        else:
            boards.append(np.array(board, dtype=int))
            board = []
    boards.append(np.array(board, dtype=int))
    return boards


if __name__ == "__main__":
    main()
