import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(4, 2021)


def main():
    lines = advent.get_input_lines()
    draws = [int(i) for i in lines[0].split(",")]
    boards = get_boards(lines[2:])

    b, m, d = first_winner(draws, boards)
    total = d * b[~m].sum()
    advent.submit(1, total)

    winners, winner_draws = get_winners(draws, boards)
    d = winner_draws[-1]
    m, b = winners[-1]
    total = d * b[~m].sum()
    advent.submit(2, total)


def get_winners(
    draws: list[int], boards: list[npt.NDArray[np.int_]]
) -> tuple[list[tuple[npt.NDArray[np.int_], npt.NDArray[np.bool_]]], list[int]]:
    masks = [b < 0 for b in boards]
    winner_draws = []
    winners = []
    for d in draws:
        masks = [m | (b == d) for m, b in zip(masks, boards)]

        new_winners = [(m, b) for m, b in zip(masks, boards) if winner(m)]
        boards = [b for m, b in zip(masks, boards) if not winner(m)]
        masks = [m for m in masks if not winner(m)]
        if len(new_winners) > 0:
            winners.extend(new_winners)
            winner_draws.append(d)

    return winners, winner_draws


def first_winner(  # type: ignore
    draws: list[int], boards: list[npt.NDArray[np.int_]]
) -> tuple[npt.NDArray[np.int_], npt.NDArray[np.bool_], int]:
    masks = [b < 0 for b in boards]
    for d in draws:
        masks = [m | (b == d) for m, b in zip(masks, boards)]
        for i, m in enumerate(masks):
            if winner(m):
                return boards[i], masks[i], d


def winner(m: npt.NDArray[np.bool_]) -> bool:
    return (m.astype(int).sum(axis=0) == 5).any() or (
        m.astype(int).sum(axis=1) == 5
    ).any()


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
