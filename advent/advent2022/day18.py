from collections import deque
from collections.abc import Iterable

from advent2022.utils.utils import Advent

advent = Advent(18)

dirs = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}


def main():
    lines = advent.get_input_lines()
    cubes = {tuple([int(x) for x in line.split(",")]) for line in lines}
    advent.submit(1, surface_area(cubes))

    mm = min_max(cubes)
    advent.submit(2, flood_3d(cubes, mm))


def min_max(cubes: Iterable[tuple[int, ...]]) -> tuple[tuple[int, int], ...]:
    mm = tuple(
        (min([c[i] for c in cubes]) - 1, max([c[i] for c in cubes]) + 1) for i in range(3)
    )
    return mm


def flood_3d(
    cubes: Iterable[tuple[int, ...]],
    minmax: tuple[tuple[int, int], ...],
    origin=(0, 0, 0),
) -> int:
    visited = set()
    queue = deque([origin])
    surface = 0
    while queue:
        node = queue.popleft()
        visited.add(node)
        for dir in dirs:
            neighbor = tuple(node[i] + dir[i] for i in range(3))
            if all([minmax[i][0] <= neighbor[i] <= minmax[i][1] for i in range(3)]):
                if neighbor not in visited and neighbor not in queue:
                    if neighbor in cubes:
                        surface += 1
                    else:
                        queue.append(neighbor)

    return surface


def surface_area(cubes: Iterable[tuple[int, ...]]) -> int:
    surface = 0
    for cube in cubes:
        for dir in dirs:
            neighbor = tuple(cube[i] + dir[i] for i in range(3))
            if neighbor not in cubes:
                surface += 1
    return surface


if __name__ == "__main__":
    main()
