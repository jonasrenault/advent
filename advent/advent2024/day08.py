from itertools import combinations

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(8, 2024)


def main():
    lines = advent.get_input_lines()
    map = np.array([[c for c in line] for line in lines])
    antennas = [(x, y, map[(x, y)]) for x, y in zip(*np.where(map != "."))]

    antinodes = get_antinodes(map, antennas)
    advent.submit(1, len(antinodes))

    antinodes2 = get_antinodes2(map, antennas)
    advent.submit(2, len(antinodes2))


def get_antinodes2(
    map: npt.NDArray[np.str_], antennas: list[tuple[int, int, str]]
) -> set[tuple[int, int]]:
    locations: set[tuple[int, int]] = set()
    xmax, ymax = map.shape
    for (x1, y1, f1), (x2, y2, f2) in combinations(antennas, 2):
        if f1 == f2:
            for ax, ay in antinode2((x1, y1), (x2, y2), xmax, ymax):
                locations.add((ax, ay))
    return locations


def antinode2(
    a1: tuple[int, int], a2: tuple[int, int], xmax, ymax
) -> list[tuple[int, int]]:
    x1, y1 = a1
    x2, y2 = a2
    antinodes = [a1, a2]
    step = 1

    while 0 <= x1 + step * (x1 - x2) < xmax and 0 <= y1 + step * (y1 - y2) < ymax:
        antinodes.append((x1 + step * (x1 - x2), y1 + step * (y1 - y2)))
        step += 1
    step = 1
    while 0 <= x2 + step * (x2 - x1) < xmax and 0 <= y2 + step * (y2 - y1) < ymax:
        antinodes.append((x2 + step * (x2 - x1), y2 + step * (y2 - y1)))
        step += 1

    return antinodes


def get_antinodes(
    map: npt.NDArray[np.str_], antennas: list[tuple[int, int, str]]
) -> set[tuple[int, int]]:
    locations: set[tuple[int, int]] = set()
    xmax, ymax = map.shape
    for (x1, y1, f1), (x2, y2, f2) in combinations(antennas, 2):
        if f1 == f2:
            for ax, ay in antinode((x1, y1), (x2, y2)):
                if 0 <= ax < xmax and 0 <= ay < ymax:
                    locations.add((ax, ay))
    return locations


def antinode(
    a1: tuple[int, int], a2: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    x1, y1 = a1
    x2, y2 = a2
    anti1 = (2 * x1 - x2, 2 * y1 - y2)
    anti2 = (2 * x2 - x1, 2 * y2 - y1)
    return (anti1, anti2)


if __name__ == "__main__":
    main()
