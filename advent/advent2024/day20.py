import heapq

import numpy as np
import numpy.typing as npt

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
    cheats = find_cheats(grid, path)
    advent.submit(1, len([node for node, cheat in cheats.items() if cheat >= 100]))


def find_cheats(
    grid: npt.NDArray[np.str_], path: list[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    cheats = dict()
    indices = {node: i for i, node in enumerate(path)}
    for x in range(1, grid.shape[0] - 1):
        for y in range(1, grid.shape[1] - 1):
            if grid[(x, y)] == "#":
                ns = [indices[n] for n in neighbors(grid, (x, y)) if n in indices]
                if len(ns) > 1 and max(ns) - min(ns) > 2:
                    cheats[(x, y)] = max(ns) - min(ns) - 2

    return cheats


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
