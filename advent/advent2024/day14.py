import re

from advent.utils.utils import Advent

advent = Advent(14, 2024)


def main():
    lines = advent.get_input_lines()
    robots = [tuple(map(int, re.findall(r"-?\d+", line))) for line in lines]
    for _ in range(100):
        robots = step(robots, 101, 103)

    advent.submit(1, score(robots, 101, 103))


def score(robots: list[tuple[int, int, int, int]], maxx: int, maxy: int) -> int:
    s0 = len([(x, y) for x, y, _, _ in robots if x < maxx // 2 and y < maxy // 2])
    s1 = len([(x, y) for x, y, _, _ in robots if x > maxx // 2 and y < maxy // 2])
    s2 = len([(x, y) for x, y, _, _ in robots if x > maxx // 2 and y > maxy // 2])
    s3 = len([(x, y) for x, y, _, _ in robots if x < maxx // 2 and y > maxy // 2])
    return s0 * s1 * s2 * s3


def step(
    robots: list[tuple[int, int, int, int]], maxx: int, maxy: int
) -> list[tuple[int, int, int, int]]:
    updated = []
    for x, y, vx, vy in robots:
        updated.append(((x + vx) % maxx, (y + vy) % maxy, vx, vy))
    return updated


if __name__ == "__main__":
    main()
