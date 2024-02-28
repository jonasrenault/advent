import re

import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(22)

chr_to_int = {" ": 1, ".": 0, "#": 2}
dirs = {
    0: (0, 1),  # >
    1: (1, 0),  # v
    2: (0, -1),  # <
    3: (-1, 0),  # ^
}


def main():
    input = advent.get_input()
    lines = input.rstrip("\n").split("\n")
    board = get_board(lines[:-2])
    instructions = lines[-1]
    advent.submit(1, run_instructions(board, instructions))


def run_instructions(board: npt.NDArray[np.int_], instructions: str) -> int:
    dir = 0
    pos = (0, np.where(board[0, :] != 1)[0].min())
    ii = re.split("([LR])", instructions)
    for i in ii:
        try:
            i = int(i)
            pos = move(board, pos, dir, i)
        except ValueError:
            dir = (dir + 1) % 4 if i == "R" else (dir - 1) % 4
        except IndexError as e:
            print(board, pos, dir, i)
            raise e
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + dir


def move(
    board: npt.NDArray[np.int_], pos: tuple[int, int], dir: int, units: int
) -> tuple[int, int]:
    if units == 0:
        return pos

    n = neighbor(board, pos, dir)
    if board[n] == 2:
        return pos

    return move(board, n, dir, units - 1)


def neighbor(
    board: npt.NDArray[np.int_], pos: tuple[int, int], dir: int
) -> tuple[int, int]:
    d = dirs[dir]
    n = (pos[0] + d[0], pos[1] + d[1])
    if (
        n[0] >= board.shape[0]
        or n[0] < 0
        or n[1] < 0
        or n[1] >= board.shape[1]
        or board[n] == 1
    ):
        if dir == 0:
            n = (n[0], np.where(board[n[0], :] != 1)[0].min())
        elif dir == 2:
            n = (n[0], np.where(board[n[0], :] != 1)[0].max())
        elif dir == 1:
            n = (np.where(board[:, n[1]] != 1)[0].min(), n[1])
        else:
            n = (np.where(board[:, n[1]] != 1)[0].max(), n[1])
    return n


def get_board(lines: list[str]) -> npt.NDArray[np.int_]:
    max_length = max([len(line) for line in lines])
    rows = []
    for line in lines:
        rows.append([chr_to_int[c] for c in line.ljust(max_length, " ")])

    return np.array(rows, dtype=int)


if __name__ == "__main__":
    main()
