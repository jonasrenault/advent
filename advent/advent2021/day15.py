from collections import defaultdict
from heapq import heappop, heappush
from math import inf

import numpy as np
import numpy.typing as npt

from advent.utils.algos import neighbors
from advent.utils import Advent

advent = Advent(15, 2021)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=int)
    advent.submit(1, search(grid, (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1)))

    grid = tile(grid, 5)
    advent.submit(2, search(grid, (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1)))


def tile(grid: npt.NDArray[np.int_], tiles: int) -> npt.NDArray[np.int_]:
    total = np.empty((grid.shape[0] * tiles, grid.shape[1] * tiles), dtype=int)
    row_grid = grid
    col_grid = grid
    for x in range(tiles):
        for y in range(tiles):
            total[
                x * grid.shape[0] : (x + 1) * grid.shape[0],
                y * grid.shape[1] : (y + 1) * grid.shape[1],
            ] = col_grid
            col_grid = col_grid + 1
            col_grid[col_grid == 10] = 1
        row_grid = row_grid + 1
        row_grid[row_grid == 10] = 1
        col_grid = row_grid
    return total


def search(
    grid: npt.NDArray[np.int_], start: tuple[int, int], end: tuple[int, int]
) -> int:
    visited = set()
    queue = [(grid[node], node) for node in neighbors(grid, start)]
    distances: defaultdict[tuple[int, int], float] = defaultdict(lambda: inf)

    while queue:
        distance, node = heappop(queue)

        if node == end:
            return int(distance)

        if node not in visited:
            visited.add(node)

            for n in neighbors(grid, node):
                new_distance = distance + grid[n]
                if new_distance < distances[n]:
                    distances[n] = new_distance
                    heappush(queue, (new_distance, n))

    return -1


if __name__ == "__main__":
    main()
