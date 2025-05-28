import functools
from math import floor

from advent.utils import Advent

advent = Advent(5, 2024)


def main():
    lines = advent.get_input_lines()
    rules, updates = get_input(lines)
    valid, invalid = check_updates(rules, updates)
    advent.submit(1, sum([update[floor(len(update) / 2)] for update in valid]))

    fix_updates(rules, invalid)
    advent.submit(2, sum([update[floor(len(update) / 2)] for update in invalid]))


def fix_updates(rules: list[tuple[int, int]], updates: list[list[int]]):
    def compare(x: int, y: int) -> int:
        if (x, y) in rules:
            return -1
        elif (y, x) in rules:
            return 1
        return 0

    for update in updates:
        update.sort(key=functools.cmp_to_key(compare))


def check_updates(
    rules: list[tuple[int, int]], updates: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    valid = []
    invalid = []
    for update in updates:
        indices = {val: idx for idx, val in enumerate(update)}
        for left, right in rules:
            if left in indices and right in indices and indices[right] < indices[left]:
                invalid.append(update)
                break
        else:
            valid.append(update)
    return valid, invalid


def get_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            rules.append((int(line[:2]), int(line[3:])))
        elif "," in line:
            updates.append(list(map(int, line.split(","))))
    return rules, updates


if __name__ == "__main__":
    main()
