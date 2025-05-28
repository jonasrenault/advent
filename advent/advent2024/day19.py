from functools import lru_cache

from advent.utils import Advent

advent = Advent(19, 2024)


def main():
    lines = advent.get_input_lines()

    towels = tuple(lines[0].split(", "))
    patterns = lines[2:]

    advent.submit(1, len([pattern for pattern in patterns if match(pattern, towels)]))
    advent.submit(2, sum([match(pattern, towels) for pattern in patterns]))


@lru_cache(maxsize=None)
def match(pattern: str, towels: tuple[str, ...]) -> int:
    total = 0
    for towel in towels:
        if pattern == towel:
            total += 1
        elif pattern.startswith(towel):
            total += match(pattern[len(towel) :], towels)
    return total


if __name__ == "__main__":
    main()
