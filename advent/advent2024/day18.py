import heapq

import numpy as np
import numpy.typing as npt

from advent.utils.algos import neighbors
from advent.utils.utils import Advent

advent = Advent(18, 2024)


def main():
    lines = advent.get_input_lines()
    grid = np.full((71, 71), ".")

    corrupted = [tuple(map(int, line.split(","))) for line in lines]
    for node in corrupted[:1024]:
        grid[node] = "#"

    start = (0, 0)
    end = (70, 70)
    advent.submit(1, dijkstra(grid, start, end))

    for node in corrupted[1024:]:
        grid[node] = "#"

    for node in corrupted[::-1]:
        grid[node] = "."
        if dijkstra(grid, start, end) is not None:
            break

    advent.submit(2, ",".join(map(str, node)))


def dijkstra(
    grid: npt.NDArray[np.str_],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int | None:
    visited = set()
    distance = {start: 0}
    queue = [(0, start)]

    while queue:
        dist, node = heapq.heappop(queue)

        if node == end:
            return dist

        if node not in visited:
            visited.add(node)

            for neighbor in neighbors(grid, node):
                if grid[neighbor] != "#":
                    new_dist = dist + 1
                    if neighbor not in distance or new_dist < distance[neighbor]:
                        distance[neighbor] = new_dist
                        heapq.heappush(queue, (new_dist, neighbor))

    return None


if __name__ == "__main__":
    main()
