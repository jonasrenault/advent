from collections.abc import Callable, Iterator
from math import ceil

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(21, 2023)

deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines], dtype=str)
    advent.submit(1, len(solve(grid, 64, neighbors)))

    H, W = grid.shape
    mod = 26501365 % H
    a = len(solve(grid, mod, neighbors_inf))
    b = len(solve(grid, mod + H, neighbors_inf))
    c = len(solve(grid, mod + 2 * H, neighbors_inf))
    first_diff1 = b - a
    first_diff2 = c - b
    second_diff = first_diff2 - first_diff1
    A = second_diff // 2
    B = first_diff1 - 3 * A
    C = a - B - A
    f = lambda n: A * n**2 + B * n + C  # noqa: E731
    ans2 = f(ceil(26501365 / H))
    advent.submit(2, ans2)


def solve(
    grid: npt.NDArray[np.str_],
    steps: int,
    neighbor_f: Callable[
        [npt.NDArray[np.str_], tuple[int, int]], Iterator[tuple[int, int]]
    ],
) -> set[tuple[int, int]]:
    start = np.where(grid == "S")
    start = start[0][0], start[1][0]
    n1: set[tuple[int, int]] = set()
    n2: set[tuple[int, int]] = set()
    current = {start}
    for _ in tqdm(range(steps)):
        new_nodes = next_nodes(grid, current, n1, n2, neighbor_f)
        n2 = n1
        n1 = current
        current = new_nodes
    return current


def next_nodes(
    grid: npt.NDArray[np.str_],
    current: set[tuple[int, int]],
    n1: set[tuple[int, int]],
    n2: set[tuple[int, int]],
    neighbor_f: Callable[
        [npt.NDArray[np.str_], tuple[int, int]], Iterator[tuple[int, int]]
    ],
) -> set[tuple[int, int]]:
    new_nodes = set()
    for node in current - n2:
        for neighbor in neighbor_f(grid, node):
            new_nodes.add(neighbor)

    return new_nodes | n1


def neighbors_inf(
    grid: npt.NDArray[np.str_], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    H, W = grid.shape
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if grid[(rr % H, rc % W)] != "#":
            yield rr, rc


def neighbors(
    grid: npt.NDArray[np.str_], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc and grid[(rr, rc)] != "#":
            yield (rr, rc)


if __name__ == "__main__":
    main()
