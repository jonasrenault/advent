import re

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(22)

WALL = "#"
FREE = "."
EMPTY = " "
RIGHT, DOWN, LEFT, UP = range(4)

DIRMAP = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

FACES = (
    (1, 50, 51, 100),
    (1, 50, 101, 150),
    (51, 100, 51, 100),
    (101, 150, 1, 50),
    (101, 150, 51, 100),
    (151, 200, 1, 50),
)


def main():
    input = advent.get_input()
    lines = input.rstrip("\n").split("\n")
    board = get_padded_board(lines[:-2])
    instructions = lines[-1]

    advent.submit(1, walk_grid(board, instructions))
    advent.submit(2, walk_cube(board, instructions))


def walk_cube(board: npt.NDArray[np.str_], instructions: str) -> int:
    d = RIGHT
    r = 1
    c = np.where(board[1, :] != EMPTY)[0].min()
    moves = re.split("([LR])", instructions)

    for move in moves:
        if move == "L":
            d = (d - 1) % 4
        elif move == "R":
            d = (d + 1) % 4
        else:
            for _ in range(int(move)):
                newr, newc, newd = move_cube(board, r, c, d)
                if board[newr][newc] == WALL:
                    break

                r, c, d = newr, newc, newd

    return 1000 * r + 4 * c + d


def face(r: int, c: int) -> tuple[int, int, int]:
    for face_id, (rmin, rmax, cmin, cmax) in enumerate(FACES, 1):
        if rmin <= r <= rmax and cmin <= c <= cmax:
            return face_id, r - rmin + 1, c - cmin + 1
    return -1, r, c


def move_cube(
    board: npt.NDArray[np.str_], r: int, c: int, dir: int
) -> tuple[int, int, int]:
    dr, dc = DIRMAP[dir]
    newr = r + dr
    newc = c + dc

    if board[newr, newc] != EMPTY:
        return newr, newc, dir

    # We fell off an edge, we need to wrap to another face...
    face_id, fr, fc = face(r, c)
    # fr = face-relative row (from the top left of the face)
    # fc = face-relative column (from the top left of the face)

    if face_id == 1:
        if dir == UP:  # face 6 going right
            return fc + 150, 1, RIGHT
        # direction == LEFT        -> face 4 going right
        return (51 - fr) + 100, 1, RIGHT

    if face_id == 2:
        if dir == UP:  # face 6 going up
            return 200, fc, UP
        if dir == DOWN:  # face 3 going left
            return fc + 50, 100, LEFT
        # direction == RIGHT       -> face 5 going left
        return (51 - fr) + 100, 100, LEFT

    if face_id == 3:
        if dir == LEFT:  # face 4 going down
            return 101, fr, DOWN
        # direction == RIGHT       -> face 2 going up
        return 50, fr + 100, UP

    if face_id == 4:
        if dir == UP:  # face 3 going right
            return fc + 50, 51, RIGHT
        # direction == LEFT        -> face 1 going right
        return (51 - fr), 51, RIGHT

    if face_id == 5:
        if dir == RIGHT:  # face 2 going left
            return (51 - fr), 150, LEFT
        # direction == DOWN        -> face 6 going left
        return fc + 150, 50, LEFT

    # face_id == 6
    if dir == LEFT:  # face 1 going down
        return 1, fr + 50, DOWN
    if dir == RIGHT:  # face 5 going up
        return 150, fr + 50, UP
    else:  # direction == DOWN      -> face 2 going down
        return 1, fc + 100, DOWN


def walk_grid(board: npt.NDArray[np.str_], instructions: str) -> int:
    d = RIGHT
    r = 1
    c = np.where(board[1, :] != EMPTY)[0].min()
    moves = re.split("([LR])", instructions)

    for move in moves:
        if move == "L":
            d = (d - 1) % 4
        elif move == "R":
            d = (d + 1) % 4
        else:
            for _ in range(int(move)):
                newr, newc, newd = move_grid(board, r, c, d)
                if board[newr][newc] == WALL:
                    break

                r, c, d = newr, newc, newd

    return 1000 * r + 4 * c + d


def move_grid(
    board: npt.NDArray[np.str_], r: int, c: int, direction: int
) -> tuple[int, int, int]:
    dr, dc = DIRMAP[direction]
    r += dr
    c += dc

    if board[r][c] == EMPTY:
        if direction == RIGHT:
            c = np.where(board[r, :] != EMPTY)[0].min()
        elif direction == LEFT:
            c = np.where(board[r, :] != EMPTY)[0].max()
        elif direction == DOWN:
            r = np.where(board[:, c] != EMPTY)[0].min()
        else:
            r = np.where(board[:, c] != EMPTY)[0].max()

    return r, c, direction


def get_padded_board(lines: list[str]) -> npt.NDArray[np.str_]:
    max_length = max([len(line) for line in lines])
    rows = [[EMPTY] * (max_length + 2)]
    for line in lines:
        rows.append([EMPTY] + [c for c in line.ljust(max_length, " ")] + [EMPTY])

    rows.append([EMPTY] * (max_length + 2))
    return np.array(rows, dtype=str)


if __name__ == "__main__":
    main()
