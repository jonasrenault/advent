from collections import deque

import numpy as np
import numpy.typing as npt

from advent.utils.algos import deltas_4
from advent.utils.utils import Advent

advent = Advent(12, 2024)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    regions = get_regions(grid)

    advent.submit(
        1, sum([len(region) * get_perimeter(grid, region) for region in regions])
    )

    advent.submit(2, sum([len(region) * get_sides(grid, region) for region in regions]))


def get_sides(grid: npt.NDArray[np.str_], region: set[tuple[int, int]]) -> int:
    maxx = grid.shape[0] - 1
    maxy = grid.shape[1] - 1
    sides = 0
    for dx, dy in deltas_4:
        nodes = set()
        for x, y in region:
            rx, ry = x + dx, y + dy
            if (
                rx < 0
                or rx > maxx
                or ry < 0
                or ry > maxy
                or grid[(rx, ry)] != grid[(x, y)]
            ):
                nodes.add((x, y))
        sides += len(get_regions(grid, nodes))
    return sides


def get_perimeter(grid: npt.NDArray[np.str_], region: set[tuple[int, int]]) -> int:
    maxx = grid.shape[0] - 1
    maxy = grid.shape[1] - 1
    peri = 0
    for x, y in region:
        for dx, dy in deltas_4:
            rx, ry = x + dx, y + dy
            if (
                rx < 0
                or rx > maxx
                or ry < 0
                or ry > maxy
                or grid[(rx, ry)] != grid[(x, y)]
            ):
                peri += 1
    return peri


def get_regions(
    grid: npt.NDArray[np.str_], nodes: set[tuple[int, int]] | None = None
) -> list[set[tuple[int, int]]]:
    regions: list[set[tuple[int, int]]] = []
    if nodes is None:
        nodes = set([(x, y) for x in range(grid.shape[0]) for y in range(grid.shape[1])])

    while nodes:
        node = nodes.pop()
        region = get_region(grid, nodes, node)
        nodes = nodes - region
        regions.append(region)

    return regions


def get_region(
    grid: npt.NDArray[np.str_], nodes: set[tuple[int, int]], start: tuple[int, int]
) -> set[tuple[int, int]]:
    region = set()
    queue: deque[tuple[int, int]] = deque([start])

    while queue:
        node = queue.popleft()
        if node not in region:
            region.add(node)
            for n in neighbors(nodes, node):
                if grid[n] == grid[start]:
                    queue.append(n)

    return region


def neighbors(nodes: set[tuple[int, int]], node: tuple[int, int]):
    r, c = node
    for dr, dc in deltas_4:
        rr, rc = r + dr, c + dc
        if (rr, rc) in nodes:
            yield (rr, rc)


if __name__ == "__main__":
    main()
