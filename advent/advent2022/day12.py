import heapq
from collections.abc import Callable, Iterator

import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(12)

deltas_4 = ((-1, 0), (0, -1), (0, 1), (1, 0))


def main():
    lines = advent.get_input_lines()

    heightmap = [[ord(c) for c in line] for line in lines]
    heightmap = np.array(heightmap, dtype=int)
    start = tuple(np.argwhere(heightmap == ord("S"))[0])
    end = tuple(np.argwhere(heightmap == ord("E"))[0])
    heightmap[start] = ord("a")
    heightmap[end] = ord("z")

    advent.submit(
        1,
        dijkstra(
            heightmap, start, {end}, lambda height1, height2: height2 <= height1 + 1
        ),
    )

    ends = np.argwhere(heightmap == ord("a"))
    ends = set([tuple(x) for x in ends])
    advent.submit(
        2, dijkstra(heightmap, end, ends, lambda height1, height2: height1 <= height2 + 1)
    )


def neighbors(
    grid: npt.NDArray[np.int_],
    node: tuple[int, int],
    height_cond: Callable[[int, int], bool],
) -> Iterator[tuple[int, int]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if (
            0 <= rr <= maxr
            and 0 <= rc <= maxc
            and height_cond(grid[(r, c)], grid[rr, rc])
        ):
            yield (rr, rc)


def dijkstra(
    heightmap: npt.NDArray[np.int_],
    start: tuple[int, int],
    ends: set[tuple[int, int]],
    height_cond: Callable[[int, int], bool],
) -> int | None:
    visited = set()
    distance = {start: 0}
    queue = [(0, start)]

    while queue:
        dist, node = heapq.heappop(queue)

        if node in ends:
            return dist

        if node not in visited:
            visited.add(node)

            for neighbor in neighbors(heightmap, node, height_cond):
                new_dist = dist + 1
                if neighbor not in distance or new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor))

    return None


if __name__ == "__main__":
    main()
