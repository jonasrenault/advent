from collections.abc import Iterator

import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(24, 2022)

dirs = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))


def main():
    lines = advent.get_input_lines()
    valley = np.array([[c for c in line] for line in lines], dtype=str)
    blizzards = get_blizzards(valley)

    start = (0, 1)
    end = (valley.shape[0] - 1, valley.shape[1] - 2)
    advent.submit(1, bfs(valley, blizzards, start, end))


def bfs(
    valley: npt.NDArray[np.str_],
    blizzards: set[tuple[int, int, str]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    positions = {start}
    time = 0

    while end not in positions:
        time += 1
        blizzards = move_blizzards(blizzards, valley.shape)
        positions = set(advance(valley, blizzard_positions(blizzards), positions))

    return time


def advance(
    valley: npt.NDArray[np.str_],
    blizzard_positions: set[tuple[int, int]],
    positions: set[tuple[int, int]],
):
    for position in positions:
        yield from neighbors(valley, blizzard_positions, position)


def neighbors(
    valley: npt.NDArray[np.str_],
    blizzard_positions: set[tuple[int, int]],
    node: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = valley.shape[0] - 1
    maxc = valley.shape[1] - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if (
            0 <= rr <= maxr
            and 0 <= rc <= maxc
            and valley[(rr, rc)] != "#"
            and (rr, rc) not in blizzard_positions
        ):
            yield (rr, rc)

    if (r, c) not in blizzard_positions:
        yield (r, c)


def blizzard_positions(blizzards: set[tuple[int, int, str]]) -> set[tuple[int, int]]:
    return set([(x, y) for x, y, _ in blizzards])


def move_blizzards(
    blizzards: set[tuple[int, int, str]], valley_shape: tuple[int, int]
) -> set[tuple[int, int, str]]:
    return set([move_blizzard(blizzard, valley_shape) for blizzard in blizzards])


def move_blizzard(
    blizzard: tuple[int, int, str], valley_shape: tuple[int, int]
) -> tuple[int, int, str]:
    r, c = valley_shape
    x, y, dir = blizzard
    dx, dy = dirs[dir]
    if (x + dx) == 0:
        return r - 2, y, dir
    if (x + dx) == r - 1:
        return 1, y, dir
    if (y + dy) == 0:
        return x, c - 2, dir
    if (y + dy) == c - 1:
        return x, 1, dir
    return x + dx, y + dy, dir


def get_blizzards(valley: npt.NDArray[np.str_]) -> set[tuple[int, int, str]]:
    blizzards: set[tuple[int, int, str]] = set()
    for dir in (">", "<", "v", "^"):
        for x, y in zip(*np.where(valley == dir)):
            blizzards.add((x, y, dir))
    return blizzards


# def draw_blizzards(valley, blizzards):
#     grid = np.full(valley.shape, ".")
#     grid[:, 0] = "#"
#     grid[:, -1] = "#"
#     grid[0, 2:] = "#"
#     grid[-1, :-2] = "#"
#     for x, y, dir in blizzards:
#         if grid[x, y] == ".":
#             grid[x, y] = dir
#         elif grid[x, y] in dirs:
#             grid[x, y] = "2"
#         else:
#             grid[x, y] = str(1 + int(grid[x, y]))

#     return grid


if __name__ == "__main__":
    main()
