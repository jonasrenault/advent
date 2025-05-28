from math import cos, radians, sin

from advent.utils import Advent

advent = Advent(12, 2020)


DIRS = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0),
    90: (1, 0),
    180: (0, -1),
    270: (-1, 0),
    0: (0, 1),
}


def main():
    lines = advent.get_input_lines()
    pos = run(lines)
    advent.submit(1, abs(pos[0]) + abs(pos[1]))

    pos = run_wp(lines)
    advent.submit(2, abs(pos[0]) + abs(pos[1]))


def run(instructions: list[str]) -> tuple[int, int]:
    heading = 90
    pos = (0, 0)
    for i in instructions:
        d = i[0]
        v = int(i[1:])
        if d == "R":
            heading = (heading + v) % 360
        elif d == "L":
            heading = (heading - v) % 360
        elif d == "F":
            offset = DIRS[heading]
            pos = pos[0] + v * offset[0], pos[1] + v * offset[1]
        else:
            offset = DIRS[d]
            pos = pos[0] + v * offset[0], pos[1] + v * offset[1]
    return pos


def run_wp(instructions: list[str]) -> tuple[int, int]:
    pos = (0, 0)
    wp = (10, 1)
    for i in instructions:
        d = i[0]
        v = int(i[1:])
        if d == "R":
            wp = rotate(wp, radians(-v))
        elif d == "L":
            wp = rotate(wp, radians(v))
        elif d == "F":
            pos = pos[0] + v * wp[0], pos[1] + v * wp[1]
        else:
            offset = DIRS[d]
            wp = wp[0] + v * offset[0], wp[1] + v * offset[1]
    return pos


def rotate(point: tuple[int, int], angle: float) -> tuple[int, int]:
    x, y = point
    qx = cos(angle) * (x) - sin(angle) * (y)
    qy = sin(angle) * (x) + cos(angle) * (y)
    return round(qx), round(qy)


if __name__ == "__main__":
    main()
