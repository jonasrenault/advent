from collections import defaultdict
from itertools import permutations, product
from typing import TypeAlias

from advent.utils.algos import manhattan
from advent.utils.utils import Advent

advent = Advent(19, 2021)


Point: TypeAlias = tuple[int, ...]
Orientation: TypeAlias = tuple[Point, Point]

ORIENTATIONS: list[Orientation] = list(
    product(permutations((0, 1, 2), 3), product((-1, 1), repeat=3))
)


def main():
    lines = advent.get_input_lines()
    scanners = get_scanners(lines)
    positions, beacons = find_positions(scanners)
    advent.submit(1, len(beacons))

    distances = [manhattan(p1, p2) for p1, p2 in product(positions.values(), repeat=2)]
    advent.submit(2, max(distances))


def find_positions(
    scanners: dict[int, set[Point]]
) -> tuple[dict[int, Point], set[Point]]:
    """
    Find positions of scanners and beacons relative to scanner 0's position.

    Args:
        scanners (dict[int, set[Point]]): dict of scanner's relative beacon positions

    Returns:
        tuple[dict[int, Point], set[Point]]: the scanner and beacon positions
        relative to scanner 0
    """
    positions: dict[int, Point] = {0: (0, 0, 0)}
    orientations: dict[int, Orientation] = {0: ((0, 1, 2), (1, 1, 1))}
    beacons: set[Point] = scanners[0]

    while len(positions) != len(scanners):
        for s2 in set(scanners.keys()) - set(positions.keys()):
            m = get_scanner_relative_position(beacons, scanners[s2])
            if m is not None:
                s2_pos, s2_orientation = m
                positions[s2] = s2_pos
                orientations[s2] = s2_orientation
                s2_beacons = translate(scanners[s2], s2_pos, s2_orientation)
                beacons |= s2_beacons

    return positions, beacons


def get_scanner_relative_position(
    scanner1: set[Point], scanner2: set[Point]
) -> tuple[Point, Orientation] | None:
    """
    Find scanner2's position and orientation relative to scanner1.

    Args:
        scanner1 (set[Point]): scanner1 beacons
        scanner2 (set[Point]): scanner2 beacons

    Returns:
        tuple[Point, Orientation]: scanner2's position and orientation
    """
    matching_beacons: dict[tuple[Point, Orientation], int] = defaultdict(int)
    for o2 in ORIENTATIONS:
        for b1, b2 in product(scanner1, scanner2):
            s2_position: Point = tuple([x - y for x, y in zip(b1, rotate(b2, o2))])
            matching_beacons[(s2_position, o2)] += 1
    for key, value in matching_beacons.items():
        if value >= 12:
            return key
    return None


def translate(
    scanner: set[Point], scanner_position: Point, orientation: Orientation
) -> set[Point]:
    return {
        tuple([x + y for x, y in zip(scanner_position, rotate(beacon, orientation))])
        for beacon in scanner
    }


def rotate(
    point: Point,
    orientation: Orientation,
) -> Point:
    return tuple([point[i] * s for i, s in zip(*orientation)])


def get_scanners(lines: list[str]) -> dict[int, set[Point]]:
    scanners = dict()
    scanner: set[Point] = set()
    id = -1
    for line in lines:
        if "scanner" in line:
            scanner = set()
            id += 1
        elif line:
            x, y, z = line.split(",")
            scanner.add((int(x), int(y), int(z)))
        else:
            scanners[id] = scanner
    scanners[id] = scanner
    return scanners


if __name__ == "__main__":
    main()
