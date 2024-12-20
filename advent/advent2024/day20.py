import heapq
from collections import deque
from typing import Iterator

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent.utils.algos import neighbors
from advent.utils.utils import Advent

advent = Advent(20, 2024)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    start = tuple(np.argwhere(grid == "S")[0])
    end = tuple(np.argwhere(grid == "E")[0])
    grid[start] = "."
    grid[end] = "."

    _, path = dijkstra(grid, start, end)
    cheats = count_cheat_paths(grid, path, cheat_duration=2, minimum_cheat=100)
    advent.submit(1, len(cheats))

    cheats = count_cheat_paths(grid, path, cheat_duration=20, minimum_cheat=100)
    advent.submit(2, len(cheats))


def count_cheat_paths(
    grid: npt.NDArray[np.str_],
    path: list[tuple[int, int]],
    cheat_duration: int = 2,
    minimum_cheat: int = 100,
) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
    cheats = dict()
    indices = {node: i for i, node in enumerate(path)}
    for start in tqdm(path):
        for end, dist in find_cheat_paths(
            grid, start, indices, max_distance=cheat_duration
        ):
            if indices[end] - indices[start] - dist >= minimum_cheat:
                cheats[(start, end)] = indices[end] - indices[start] - dist

    return cheats


def find_cheat_paths(
    grid: npt.NDArray[np.str_],
    start: tuple[int, int],
    indices: dict[tuple[int, int], int],
    max_distance: int = 20,
) -> Iterator[tuple[tuple[int, int], int]]:
    """
    Find all possible paths starting from start node with maximum distance max_distance
    which end further on the path.

    Args:
        grid (npt.NDArray[np.str_]): the grid
        start (tuple[int, int]): start node
        indices (dict[tuple[int, int], int]): dict of path node -> index on path
        max_distance (int, optional): maximum distance. Defaults to 20.

    Yields:
        Iterator[tuple[tuple[int, int], int]]: all nodes within max_distance of start
    """
    visited = {start}
    queue: deque[tuple[int, tuple[int, int]]] = deque()

    for n in neighbors(grid, start):
        queue.append((1, n))

    while queue:
        dist, node = queue.popleft()
        if node not in visited and dist <= max_distance:
            visited.add(node)
            if node in indices and indices[node] > indices[start]:
                yield ((node), dist)
                # continue

            for n in neighbors(grid, node):
                queue.append((1 + dist, n))


def dijkstra(
    grid: npt.NDArray[np.str_],
    start: tuple[int, int],
    end: tuple[int, int],
) -> tuple[int | None, list[tuple[int, int]]]:
    visited = set()
    distance = {start: 0}
    queue = [(0, start, [start])]

    while queue:
        dist, node, path = heapq.heappop(queue)

        if node == end:
            return dist, path

        if node not in visited:
            visited.add(node)

            for neighbor in neighbors(grid, node):
                if grid[neighbor] != "#":
                    new_dist = dist + 1
                    if neighbor not in distance or new_dist < distance[neighbor]:
                        distance[neighbor] = new_dist
                        heapq.heappush(queue, (new_dist, neighbor, path + [neighbor]))

    return None, []


if __name__ == "__main__":
    main()
