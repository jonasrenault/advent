import statistics
from functools import reduce

from advent.utils import Advent

advent = Advent(10, 2021)

mapping = {"[": "]", "(": ")", "{": "}", "<": ">"}
points = {")": 3, "]": 57, "}": 1197, ">": 25137}
autocomplete_points = {")": 1, "]": 2, "}": 3, ">": 4}


def main():
    lines = advent.get_input_lines()
    advent.submit(1, sum([points[c] for c, _ in get_corrupted(lines)]))

    autocomplete_scores = [
        reduce(lambda tot, c: tot * 5 + autocomplete_points[c], ac, 0)
        for ac in autocomplete(lines)
    ]
    advent.submit(2, statistics.median(autocomplete_scores))


def autocomplete(lines: list[str]) -> list[list[str]]:
    completed = []
    for line in lines:
        chunks = []
        for c in line:
            if c in mapping.keys():
                chunks.append(c)
            else:
                expected = mapping[chunks.pop()]
                if c != expected:
                    break
        else:
            autocomplete = [mapping[c] for c in chunks[::-1]]
            completed.append(autocomplete)

    return completed


def get_corrupted(lines: list[str]) -> list[tuple[str, str]]:
    corrupt = []
    for line in lines:
        chunks = []
        for c in line:
            if c in mapping.keys():
                chunks.append(c)
            else:
                expected = mapping[chunks.pop()]
                if c != expected:
                    corrupt.append((c, line))
                    break
    return corrupt


if __name__ == "__main__":
    main()
