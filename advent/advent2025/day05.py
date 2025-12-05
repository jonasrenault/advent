from typing import cast

from advent.utils import Advent

advent = Advent(5, 2025)


def main():
    lines = advent.get_input_lines()
    ranges, ids = read_input(lines)

    advent.submit(1, len(fresh(ranges, ids)))

    ranges = merge(ranges)
    total = 0
    for left, right in ranges:
        total += right - left + 1

    advent.submit(2, total)


def merge(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge ranges which overlap.

    Args:
        ranges (list[tuple[int, int]]): a list of ranges.

    Returns:
        list[tuple[int, int]]: a list of merged ranges.
    """
    nb_ranges = len(ranges) + 1
    while nb_ranges != len(ranges):
        nb_ranges = len(ranges)
        merged: list[tuple[int, int]] = []
        for left, right in ranges:
            for idx in range(len(merged)):
                x, y = merged[idx]
                if not (x > right or y < left):
                    merged[idx] = (min(left, x), max(y, right))
                    break
            else:
                merged.append((left, right))
        ranges = merged
    return ranges


def fresh(ranges: list[tuple[int, int]], ids: list[int]) -> set[int]:
    """
    Get the set of ids which are within at least one of the ranges.

    Args:
        ranges (list[tuple[int, int]]): a list of ranges (min, max).
        ids (list[int]): a list of ids.

    Returns:
        set[int]: the set of ids which are within one of the ranges.
    """
    fresh = set()
    for id in ids:
        for left, right in ranges:
            if left <= id <= right:
                fresh.add(id)
                break

    return fresh


def read_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    ids = []
    for line in lines:
        if not line:
            continue
        if "-" in line:
            ranges.append(cast(tuple[int, int], tuple(map(int, line.split("-")))))
        else:
            ids.append(int(line))

    return ranges, ids


if __name__ == "__main__":
    main()
