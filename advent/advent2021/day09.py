from functools import reduce
from math import prod

import numpy as np
import numpy.typing as npt

from advent.utils.algos import neighbors
from advent.utils.utils import Advent

advent = Advent(9, 2021)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=int)

    lowpoints = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if all([grid[r, c] < grid[n] for n in neighbors(grid, (r, c))]):
                lowpoints.append((r, c))
    advent.submit(1, sum([grid[p] + 1 for p in lowpoints]))

    basins = [len(basin(grid, p)) for p in lowpoints]
    basins.sort()
    advent.submit(2, prod(basins[-3:]))


def basin(grid: npt.NDArray[np.int_], node: tuple[int, int]) -> set[tuple[int, int]]:
    return reduce(
        set.union,
        (
            basin(grid, neighbor)
            for neighbor in neighbors(grid, node)
            if 9 > grid[neighbor] > grid[node]
        ),
        set((node,)),
    )


if __name__ == "__main__":
    main()
