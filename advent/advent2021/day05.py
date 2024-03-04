from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(5, 2021)


def main():
    lines = advent.get_input_lines()
    coords = get_coords(lines)
    overlaps = get_overlaps(coords)
    advent.submit(1, len([c for c in overlaps.values() if c > 1]))

    overlaps = get_overlaps(coords, True)
    advent.submit(2, len([c for c in overlaps.values() if c > 1]))


def get_overlaps(
    coords: list[tuple[tuple[int, int], tuple[int, int]]], count_diag: bool = False
) -> dict[tuple[int, int], int]:
    points: dict[tuple[int, int], int] = defaultdict(lambda: 0)
    for (x0, y0), (x1, y1) in coords:
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                points[(x0, y)] += 1
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                points[(x, y0)] += 1
        elif count_diag:
            xstep = -1 if x1 < x0 else 1
            ystep = -1 if y1 < y0 else 1
            for x, y in zip(range(x0, x1 + xstep, xstep), range(y0, y1 + ystep, ystep)):
                points[x, y] += 1
    return points


def get_coords(lines: list[str]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    coords = []
    for line in lines:
        left, right = line.split("->")
        x0, y0 = left.strip().split(",")
        x1, y1 = right.strip().split(",")
        coords.append(((int(x0), int(y0)), (int(x1), int(y1))))
    return coords


if __name__ == "__main__":
    main()
