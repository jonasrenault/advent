from math import prod

from advent.utils.utils import Advent

advent = Advent(3, 2020)


def main():
    lines = advent.get_input_lines()

    advent.submit(1, check_slope(lines, (1, 3)))

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    counts = [check_slope(lines, slope) for slope in slopes]
    advent.submit(2, prod(counts))


def check_slope(lines: list[str], slope: tuple[int, int]) -> int:
    my = len(lines[0])
    sx, sy = slope
    x, y = (0, 0)
    c = 0
    while x < len(lines):
        is_tree = lines[x][y] == "#"
        if is_tree:
            c += 1
        y = (y + sy) % my
        x += sx
    return c


if __name__ == "__main__":
    main()
