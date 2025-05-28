import re

from advent.utils import Advent

advent = Advent(10, 2018)


def main():
    lines = advent.get_input_lines()
    points = [tuple(map(int, re.findall(r"([\-0-9]+)", line))) for line in lines]
    step, points = run(points)
    print_points({(x, y) for (x, y, _, _) in points})
    advent.submit(1, "XPFXXXKL")
    advent.submit(2, step)


def print_points(points: set[tuple[int, int]]):
    xmax = max([x for x, _ in points])
    xmin = min([x for x, _ in points])
    ymax = max([y for _, y in points])
    ymin = min([y for _, y in points])
    for y in range(ymin - 2, ymax + 3):
        line = ["#" if (x, y) in points else "." for x in range(xmin - 2, xmax + 3)]
        print("".join(line))


def run(points: list[tuple[int, ...]]) -> tuple[int, list[tuple[int, ...]]]:
    step = 0
    while not has_vertical_line({(x, y) for (x, y, _, _) in points}):
        points = [(x + dx, y + dy, dx, dy) for (x, y, dx, dy) in points]
        step += 1
    return step, points


def has_vertical_line(points: set[tuple[int, int]]) -> bool:
    for x, y in points:
        for dy in range(1, 6):
            if (x, y + dy) not in points:
                break
        else:
            break
    else:
        return False
    return True


if __name__ == "__main__":
    main()
