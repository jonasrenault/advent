from collections import defaultdict, deque

import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(23)


def main():
    lines = advent.get_input_lines()
    grid = get_grid(lines)
    neighbors = deque(
        [
            [(-1, 0), (-1, -1), (-1, 1)],  # north
            [(1, 0), (1, -1), (1, 1)],  # south
            [(0, -1), (-1, -1), (1, -1)],  # west
            [(0, 1), (-1, 1), (1, 1)],  # east
        ]
    )

    c = find_empty_tiles(grid, neighbors, 10)
    advent.submit(1, c)

    grid = get_grid(lines)
    neighbors = deque(
        [
            [(-1, 0), (-1, -1), (-1, 1)],  # north
            [(1, 0), (1, -1), (1, 1)],  # south
            [(0, -1), (-1, -1), (1, -1)],  # west
            [(0, 1), (-1, 1), (1, 1)],  # east
        ]
    )
    c = count_rounds(grid, neighbors)
    advent.submit(2, c)


def count_rounds(
    grid: npt.NDArray[np.int_], neighbors: deque[list[tuple[int, int]]]
) -> int:
    count = 0
    moved = True
    while moved:
        moved = move(grid, neighbors)
        count += 1

    return count


def find_empty_tiles(
    grid: npt.NDArray[np.int_], neighbors: deque[list[tuple[int, int]]], moves: int
):
    neighbors = deque(
        [
            [(-1, 0), (-1, -1), (-1, 1)],  # north
            [(1, 0), (1, -1), (1, 1)],  # south
            [(0, -1), (-1, -1), (1, -1)],  # west
            [(0, 1), (-1, 1), (1, 1)],  # east
        ]
    )
    for _ in range(moves):
        move(grid, neighbors)

    ones = np.where(grid == 1)
    slice = grid[ones[0].min() : ones[0].max() + 1, ones[1].min() : ones[1].max() + 1]
    return np.count_nonzero(slice == 0)


def move(grid: npt.NDArray[np.int_], neighbors: deque[list[tuple[int, int]]]) -> bool:
    elves = np.where(grid == 1)
    propositions = defaultdict(list)
    for x, y in zip(elves[0], elves[1]):
        if has_neighbor(grid, (x, y)):
            for option in neighbors:
                if all([grid[x + a, y + b] == 0 for a, b in option]):
                    propositions[(x + option[0][0], y + option[0][1])].append((x, y))
                    break

    moved = False
    for to, fr in propositions.items():
        if len(fr) == 1:
            grid[to] = 1
            grid[fr[0]] = 0
            moved = True

    neighbors.append(neighbors.popleft())
    return moved


def has_neighbor(grid: npt.NDArray[np.int_], coords: tuple[int, int]):
    x, y = coords
    for a, b in [(-1, 0), (-1, -1), (-1, 1), (1, 0), (1, -1), (1, 1), (0, 1), (0, -1)]:
        if 0 <= (x + a) < grid.shape[0] and 0 <= (y + b) < grid.shape[1]:
            if grid[(x + a, y + b)] == 1:
                return True
    return False


def get_grid(lines: list[str]) -> npt.NDArray[np.int_]:
    grid = np.array([[0 if c == "." else 1 for c in line] for line in lines], dtype=int)
    grid = np.concatenate(
        [
            np.concatenate([np.zeros(grid.shape, dtype=int) for _ in range(3)], axis=1),
            np.concatenate(
                [np.zeros(grid.shape, dtype=int), grid, np.zeros(grid.shape, dtype=int)],
                axis=1,
            ),
            np.concatenate([np.zeros(grid.shape, dtype=int) for _ in range(3)], axis=1),
        ],
        axis=0,
        dtype=int,
    )
    return grid


if __name__ == "__main__":
    main()
