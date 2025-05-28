from itertools import product

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent.utils import Advent

advent = Advent(11, 2021)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=int)

    flashes = 0
    runs = 100
    for _ in tqdm(range(runs)):
        grid, c = step(grid)
        flashes += c
    advent.submit(1, flashes)

    grid = np.array([[int(c) for c in line] for line in lines], dtype=int)
    flashes = 0
    count = 0
    while flashes != grid.size:
        grid, flashes = step(grid)
        count += 1
    advent.submit(2, count)


def step(grid: npt.NDArray[np.int_]) -> tuple[npt.NDArray[np.int_], int]:
    grid = grid + 1
    tens = np.argwhere(grid == 10)
    counts = 0
    for x, y in tens:
        counts += flash(grid, (x, y))
    grid[grid > 9] = 0
    return grid, counts


def flash(grid: npt.NDArray[np.int_], node: tuple[int, int]) -> int:
    """
    Flash a point and its neighbors.
    """
    x, y = node
    counts = 1
    for a, b in product((-1, 0, 1), (-1, 0, 1)):
        x0, y0 = x + a, y + b
        if 0 <= x0 < grid.shape[0] and 0 <= y0 < grid.shape[1]:
            grid[x0, y0] += 1
            if grid[x0, y0] == 10:
                counts += flash(grid, (x0, y0))
    return counts


if __name__ == "__main__":
    main()
