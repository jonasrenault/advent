from collections import defaultdict
from operator import itemgetter

from advent.utils import Advent, manhattan

advent = Advent(6, 2018)


def main():
    lines = advent.get_input_lines()
    points = [tuple(map(int, line.split(","))) for line in lines]

    areas = get_areas(points)
    areas_10 = get_areas(points, 10)
    finite = {
        key: value for key, value in areas.items() if set(areas_10[key]) == set(value)
    }

    greatest = 0
    for area in finite.values():
        if len(area) > greatest:
            greatest = len(area)
    advent.submit(1, greatest)

    count = count_safe_area(points, 50)
    advent.submit(2, count)


def get_areas(
    points: list[tuple[int, ...]], margin: int = 1
) -> dict[tuple[int, ...], list[tuple[int, int]]]:
    areas = defaultdict(list)
    xmax = max([x for (x, _) in points])
    ymax = max([y for (_, y) in points])
    for x in range(-1 * margin, xmax + margin):
        for y in range(-1 * margin, ymax + margin):
            distances_to_points = [(point, manhattan((x, y), point)) for point in points]
            distances = [d for _, d in distances_to_points]
            targetmin, dmin = min(distances_to_points, key=itemgetter(1))
            if distances.count(dmin) == 1:
                areas[targetmin].append((x, y))

    return areas


def count_safe_area(
    points: list[tuple[int, ...]], margin: int = 1, max_distances: int = 10000
) -> int:
    xmax = max([x for (x, _) in points])
    ymax = max([y for (_, y) in points])
    count = 0
    for x in range(-1 * margin, xmax + margin):
        for y in range(-1 * margin, ymax + margin):
            distances = [manhattan((x, y), point) for point in points]
            if sum(distances) < max_distances:
                count += 1
    return count


if __name__ == "__main__":
    main()
