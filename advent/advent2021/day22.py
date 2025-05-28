import re

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(22, 2021)


def main():
    lines = advent.get_input_lines()
    instructions = get_instructions(lines)
    reactor = initialize(instructions)
    advent.submit(1, np.count_nonzero(reactor))

    on, off = reboot(instructions)
    advent.submit(
        2, sum([volume(cube) for cube in on]) - sum([volume(cube) for cube in off])
    )


def volume(cube: tuple[int, ...]) -> int:
    x1, x2, y1, y2, z1, z2 = cube
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


def reboot(
    instructions: list[tuple[bool, tuple[int, ...]]],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    positive: list[tuple[int, ...]] = []
    negative: list[tuple[int, ...]] = []

    for on, cube in instructions:
        new_negative = []
        for other in positive:
            inter = intersection(cube, other)
            if inter is None:
                continue
            new_negative.append(inter)

        for other in negative:
            inter = intersection(cube, other)
            if inter is None:
                continue
            positive.append(inter)

        negative.extend(new_negative)

        if on:
            positive.append(cube)

    return positive, negative


def intersection(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...] | None:
    ax1, ax2, ay1, ay2, az1, az2 = a
    bx1, bx2, by1, by2, bz1, bz2 = b

    ix1, ix2 = max(ax1, bx1), min(ax2, bx2)
    iy1, iy2 = max(ay1, by1), min(ay2, by2)
    iz1, iz2 = max(az1, bz1), min(az2, bz2)

    if ix1 < ix2 and iy1 < iy2 and iz1 < iz2:
        return ix1, ix2, iy1, iy2, iz1, iz2

    return None


def initialize(instructions: list[tuple[bool, tuple[int, ...]]]) -> npt.NDArray[np.int_]:
    reactor = np.zeros((101, 101, 101), dtype=int)
    for on, coords in instructions:
        if all([-50 <= c <= 50 for c in coords]):
            xmin, xmax, ymin, ymax, zmin, zmax = coords
            val = 1 if on else 0
            reactor[
                xmin + 50 : xmax + 51, ymin + 50 : ymax + 51, zmin + 50 : zmax + 51
            ] = val
    return reactor


def get_instructions(lines: list[str]) -> list[tuple[bool, tuple[int, ...]]]:
    return [
        (line.startswith("on"), tuple(map(int, re.findall(r"-?\d+", line))))
        for line in lines
    ]


if __name__ == "__main__":
    main()
