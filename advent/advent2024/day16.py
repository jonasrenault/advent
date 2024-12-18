import heapq
import math
from typing import Iterator

import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(16, 2024)
DIR = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}

ROTATIONS = {">": ("^v>"), "^": "<>^", "v": "<>v", "<": "^v<"}


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    start = tuple(np.argwhere(grid == "S")[0])
    end = tuple(np.argwhere(grid == "E")[0])

    cost, path = find_paths(grid, (*start, ">"), end)
    advent.submit(1, cost)
    advent.submit(2, len(path))


def neighbors(
    grid: npt.NDArray[np.int_],
    node: tuple[int, int, str],
) -> Iterator[tuple[tuple[int, int, str], int]]:
    r, c, dir = node
    maxr = grid.shape[0] - 1
    maxc = grid.shape[1] - 1

    for d, (dr, dc) in DIR.items():
        rr, rc = r + dr, c + dc
        if (
            0 <= rr <= maxr
            and 0 <= rc <= maxc
            and grid[rr, rc] != "#"
            and d in ROTATIONS[dir]
        ):
            yield (rr, rc, d), 1 if d == dir else 1001


def find_paths(
    grid: npt.NDArray[np.str_],
    start: tuple[int, int, str],
    end: tuple[int, int],
) -> tuple[float, frozenset[tuple[int, int]]]:
    distance = {start: 0}
    best_distance = math.inf
    best_path: frozenset[tuple[int, int]] = frozenset()
    r, c, _ = start
    queue = [(0, start, frozenset([(r, c)]))]

    while queue:
        dist, node, path = heapq.heappop(queue)
        r, c, _ = node
        if (r, c) == end:
            if dist < best_distance:
                best_distance = dist
                best_path = path
            elif dist == best_distance:
                best_path |= path
            continue

        if node in distance and distance[node] < dist:
            continue

        distance[node] = dist

        for neighbor, cost in neighbors(grid, node):
            nr, nc, _ = neighbor
            if (nr, nc) not in path:
                new_dist = dist + cost
                heapq.heappush(queue, (new_dist, neighbor, path | {(nr, nc)}))

    return best_distance, best_path


if __name__ == "__main__":
    main()
