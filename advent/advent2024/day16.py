import heapq

# from collections import deque
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

    res = dijkstra(grid, (*start, ">"), end)
    print(1, res)

    # for cost, path in find_paths(grid, (*start, ">"), end):
    #     print(cost, len(path))


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


# def find_paths(
#     grid: npt.NDArray[np.str_],
#     src: tuple[int, int, str],
#     end: tuple[int, int],
# ) -> Iterator[int]:
#     visited = {src}
#     r, c, _ = src
#     queue: deque[tuple[int, tuple[int, int, str], set[tuple[int, int]]]] = deque()

#     for n, cost in neighbors(grid, src):
#         queue.append((cost, n, {(r, c)}))

#     while queue:
#         dist, node, path = queue.popleft()
#         if node not in visited:
#             visited.add(node)
#             r, c, _ = node
#             if (r, c) == end:
#                 yield dist, path
#                 continue

#             for n, cost in neighbors(grid, node):
#                 queue.append((cost + dist, n, path | {(r, c)}))


def dijkstra(
    grid: npt.NDArray[np.str_],
    start: tuple[int, int, str],
    end: tuple[int, int],
) -> int | None:
    visited = set()
    distance = {start: 0}
    queue = [(0, start)]

    while queue:
        dist, node = heapq.heappop(queue)
        r, c, _ = node
        if (r, c) == end:
            return dist

        if node not in visited:
            visited.add(node)

            for neighbor, cost in neighbors(grid, node):
                new_dist = dist + cost
                if neighbor not in distance or new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor))

    return None


if __name__ == "__main__":
    main()
