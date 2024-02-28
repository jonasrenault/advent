import re

from tqdm import tqdm

from advent2022.utils.utils import Advent

advent = Advent(15)


def main():
    lines = advent.get_input_lines()
    sensors = get_sensors(lines)
    y = 2000000
    cover = coverage(sensors, y)
    advent.submit(1, sum([manhattan((x0, y), (x1, y)) for x0, x1 in cover]))

    advent.submit(2, find_distress_signal(sensors, 4000000))


def find_distress_signal(
    sensors: dict[tuple[int, int], tuple[int, int]], limit: int
) -> int:
    """
    Find the first row within limit where the coverage is not a list of adjacent
    intervals. Compute the tuning frequency for this position.

    Parameters
    ----------
    sensors : dict[tuple[int, int], tuple[int, int]]
        The dict of sensors -> beacon
    limit : int
        the limit within which to search

    Returns
    -------
    int
        The tuning frequency equal to 4000000 * x + y
    """
    for y in tqdm(range(limit)):
        cover = coverage(sensors, y)
        if not adjacent(cover):
            return (min(cover[0][1], cover[1][1]) + 1) * 4000000 + y
    return -1


def get_sensors(lines: list[str]) -> dict[tuple[int, int], tuple[int, int]]:
    sensors = {}
    for line in lines:
        m = re.match(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        if m:
            sensors[(int(m.group(1)), int(m.group(2)))] = (
                int(m.group(3)),
                int(m.group(4)),
            )
    return sensors


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """
    Compute the manhattan or taxicab distance between points x and y.

    Parameters
    ----------
    x : tuple[int, int]
        x and y coordinates for point a
    y : tuple[int, int]
        x and y coordinates for point b

    Returns
    -------
    int
        the manhattan distance.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def overlap(i1: tuple[int, int], i2: tuple[int, int]) -> bool:
    """
    Check if two intervals overlap.

    Example
    -------
    overlap((-3, 3), (5, 10))
        False
    overlap((-3, 3), (-1, 1))
        True

    Parameters
    ----------
    i1 : tuple[int, int]
        A closed interval
    i2 : tuple[int, int]
        A closed interval

    Returns
    -------
    bool
        returns True if the intervals overlap.
    """
    return (
        i2[0] <= i1[0] <= i2[1]
        or i2[0] <= i1[1] <= i2[1]
        or i1[0] <= i2[0] <= i1[1]
        or i1[0] <= i2[1] <= i1[1]
    )


def merge_intervals(
    intervals: list[tuple[int, int]], interval: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Merge an interval into a list of other intervals, reducing the list with overlapping
    intervals.

    Parameters
    ----------
    intervals : list[tuple[int, int]]
        A list of intervals
    interval : tuple[int, int]
        An interval

    Returns
    -------
    list[tuple[int, int]]
        A list of intervals with no intervals overlapping
    """
    xmin, xmax = interval
    merged = []
    for i in intervals:
        if not overlap(i, interval):
            merged.append(i)
        else:
            xmin = min(i[0], xmin)
            xmax = max(i[1], xmax)
    return merged + [(xmin, xmax)]


def adjacent(intervals: list[tuple[int, int]]) -> bool:
    """
    Given a list of intervals, check if the intervals are adjacent.

    Example
    -------
    adjacent([(-2, 3), (4, 15)])
        True
    adjacent([(-2, 3), (5, 16)])
        False

    Parameters
    ----------
    intervals : list[tuple[int, int]]
        A list of intervals

    Returns
    -------
    bool
        True if the intervals are adjacent
    """
    adjacent = True
    for i in range(len(intervals) - 1):
        adjacent &= (
            min(
                abs(intervals[i][1] - intervals[i + 1][0]),
                abs(intervals[i][0] - intervals[i + 1][1]),
            )
            == 1
        )
    return adjacent


def coverage(
    sensors: dict[tuple[int, int], tuple[int, int]], y: int
) -> list[tuple[int, int]]:
    """
    Compute the coverage for row = y, given a dict of sensors -> beacons.

    Parameters
    ----------
    sensors : dict[tuple[int, int], tuple[int, int]]
        The dict of sensors -> beacon coordinates
    y : int
        the row coordinate

    Returns
    -------
    list[tuple[int, int]]
        The list of intervals covered by the sensors at given row
    """
    cover: list[tuple[int, int]] = []
    for s, b in sensors.items():
        d = manhattan(s, b)
        step = abs(y - s[1])
        if step <= d:
            x0, x1 = (s[0] - d + step, s[0] + d - step)
            cover = merge_intervals(cover, (x0, x1))
    return cover


if __name__ == "__main__":
    main()
