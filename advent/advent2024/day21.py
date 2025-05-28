import heapq
import math
from functools import lru_cache
from typing import Iterator, Literal

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(21, 2024)
DIR = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}

PADS: dict[str, npt.NDArray[np.str_]] = {
    "numeric": np.array(
        [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]
    ),
    "directional": np.array([["#", "^", "A"], ["<", "v", ">"]]),
}


def main():
    lines = advent.get_input_lines()

    advent.submit(1, sum(int(code[:-1]) * solve("numeric", 2, code) for code in lines))
    advent.submit(2, sum(int(code[:-1]) * solve("numeric", 25, code) for code in lines))


@lru_cache(maxsize=None)
def solve(keypad: str, robot: int, code: str, current: str = "A"):
    if not code:
        return 0

    target = code[0]
    paths = find_paths(keypad, current, target)

    if robot == 0:
        best = len(paths[0]) + 1
    else:
        best = min(solve("directional", robot - 1, p + "A") for p in paths)

    res = best + solve(keypad, robot, code[1:], target)
    return res


def neighbors(
    grid: npt.NDArray[np.str_], node: tuple[int, int]
) -> Iterator[tuple[str, tuple[int, int]]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dir, (dr, dc) in DIR.items():
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            yield dir, (rr, rc)


@lru_cache(maxsize=None)
def find_paths(
    pad: Literal["numeric", "directionnal"],
    start: str,
    target: str,
) -> list[str]:
    grid = PADS[pad]
    src = tuple(np.argwhere(grid == start)[0])
    distance = {src: 0}
    best_distance = math.inf
    best_paths: list[str] = []
    queue: list[tuple[int, tuple[int, int], str]] = [(0, src, "")]

    while queue:
        dist, node, path = heapq.heappop(queue)
        if grid[node] == target:
            if dist < best_distance:
                best_distance = dist
                best_paths = [path]
            elif dist == best_distance:
                best_paths.append(path)
            continue

        if node in distance and distance[node] < dist:
            continue

        distance[node] = dist

        for dir, neighbor in neighbors(grid, node):
            if grid[neighbor] != "#":
                new_dist = dist + 1
                heapq.heappush(queue, (new_dist, neighbor, path + dir))

    return best_paths


if __name__ == "__main__":
    main()
