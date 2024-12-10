from collections import deque
from typing import Iterator

import numpy as np
import numpy.typing as npt

from advent.utils.algos import deltas_4
from advent.utils.utils import Advent

advent = Advent(10, 2024)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[int(c) for c in line] for line in lines])

    advent.submit(
        1, sum([len(list(climb(grid, start))) for start in zip(*np.where(grid == 0))])
    )

    advent.submit(
        2, sum([len(list(climb2(grid, start))) for start in zip(*np.where(grid == 0))])
    )


def neighbors(
    grid: npt.NDArray[np.int_], node: tuple[int, int]
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc and grid[(rr, rc)] - grid[(r, c)] == 1:
            yield (rr, rc)


def climb(
    grid: npt.NDArray[np.int_], start: tuple[int, int]
) -> Iterator[tuple[tuple[int, int], int]]:
    visited = {start}
    queue: deque[tuple[int, tuple[int, int]]] = deque()

    for n in neighbors(grid, start):
        queue.append((1, n))

    while queue:
        dist, node = queue.popleft()
        if node not in visited:
            visited.add(node)
            if grid[node] == 9:
                yield ((node), dist)
                continue

            for n in neighbors(grid, node):
                queue.append((1 + dist, n))


def climb2(
    grid: npt.NDArray[np.int_], start: tuple[int, int]
) -> Iterator[tuple[tuple[int, int], set[tuple[int, int]]]]:
    visited = {start}
    queue: deque[tuple[set[tuple[int, int]], tuple[int, int]]] = deque()

    for n in neighbors(grid, start):
        queue.append((visited, n))

    while queue:
        visited, node = queue.popleft()
        if node not in visited:
            visited.add(node)
            if grid[node] == 9:
                yield (node, visited | {node})
                continue

            for n in neighbors(grid, node):
                queue.append((visited | {node}, n))


if __name__ == "__main__":
    main()
