import re
from itertools import product
from operator import itemgetter

from advent.utils.utils import Advent

advent = Advent(17, 2021)


def main():
    lines = advent.get_input_lines()
    m = re.search(
        r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", lines[0].strip()
    )
    target = [int(c) for c in m.groups()]
    mh, _ = maximum_height((0, 0), target)
    advent.submit(1, mh)

    advent.submit(2, len(all_velocities((0, 0), target)))


def all_velocities(start: tuple[int, int], target: list[int]) -> list[tuple[int, int]]:
    x0, x1, y0, y1 = target
    velocities = []
    for vx, vy in product(
        range(max(x0, x1) + 1), range(min(y0, y1), max(abs(y0), abs(y1)))
    ):
        positions = probe_positions(start, (vx, vy), target)
        if hits_target(positions, target):
            velocities.append((vx, vy))

    return velocities


def maximum_height(
    start: tuple[int, int], target: list[int]
) -> tuple[int, tuple[int, int]]:
    x0, x1, y0, y1 = target
    max_height = 0
    for vx, vy in product(range(max(x0, x1)), range(max(abs(y0), abs(y1)))):
        positions = probe_positions(start, (vx, vy), target)
        if hits_target(positions, target):
            max_y = max(positions, key=itemgetter(1))[1]
            if max_y > max_height:
                max_height = max_y
                mvx, mvy = vx, vy

    return max_height, (mvx, mvy)


def probe_positions(
    start: tuple[int, int], velocity: tuple[int, int], target: list[int]
) -> list[tuple[int, int]]:
    x, y = start
    vx, vy = velocity
    x0, x1, y0, y1 = target
    positions = [start]
    while x < max(x0, x1) and y > min(y0, y1):
        x += vx
        y += vy
        positions.append((x, y))
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return positions


def hits_target(positions: list[tuple[int, int]], target: list[int]) -> bool:
    x0, x1, y0, y1 = target
    for x, y in positions:
        if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
            return True
    return False


if __name__ == "__main__":
    main()
