import re

from advent.utils.algos import deltas_4
from advent.utils import Advent

advent = Advent(14, 2024)


def main():
    lines = advent.get_input_lines()
    robots = [tuple(map(int, re.findall(r"-?\d+", line))) for line in lines]

    positions = [move_to(*robot, 100, 101, 103) for robot in robots]
    advent.submit(1, score(positions, 101, 103))

    counts = dict()
    for t in range(10000):
        positions = set(move_to(*robot, t, 101, 103) for robot in robots)
        counts[t] = count_neighbors(positions)

    sol = max(counts, key=counts.get)
    print_bots([move_to(*robot, sol, 101, 103) for robot in robots], 101, 103)
    advent.submit(2, sol)


def print_bots(robots: set[tuple[int, int]], maxx: int, maxy: int):
    for y in range(maxy):
        print("".join(["#" if (x, y) in robots else "." for x in range(maxx)]))


def count_neighbors(robots: set[tuple[int, int]]) -> int:
    counts = 0

    for x, y in robots:
        for dx, dy in deltas_4:
            if (x + dx, y + dy) in robots:
                counts += 1

    return counts


def score(robots: list[tuple[int, int]], maxx: int, maxy: int) -> int:
    s0 = len([(x, y) for x, y in robots if x < maxx // 2 and y < maxy // 2])
    s1 = len([(x, y) for x, y in robots if x > maxx // 2 and y < maxy // 2])
    s2 = len([(x, y) for x, y in robots if x > maxx // 2 and y > maxy // 2])
    s3 = len([(x, y) for x, y in robots if x < maxx // 2 and y > maxy // 2])
    return s0 * s1 * s2 * s3


def move_to(
    x: int, y: int, vx: int, vy: int, t: int, maxx: int, maxy: int
) -> tuple[int, int]:
    return (x + vx * t) % maxx, (y + vy * t) % maxy


if __name__ == "__main__":
    main()
