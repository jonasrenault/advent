from functools import lru_cache

from advent.utils.utils import Advent

advent = Advent(19, 2024)


def main():
    lines = advent.get_input_lines()

    towels = tuple(lines[0].split(", "))
    patterns = lines[2:]

    # print(match(patterns[0], towels))
    advent.submit(1, len([pattern for pattern in patterns if match(pattern, towels)]))


@lru_cache(maxsize=None)
def match(pattern: str, towels: tuple[str, ...]) -> list[tuple[str, ...]]:
    options: list[tuple[str, ...]] = []
    for towel in towels:
        if pattern == towel:
            options.append((towel,))
            break
        elif pattern.startswith(towel):
            for subp in match(pattern[len(towel) :], towels):
                options.append((towel,) + subp)
                break

    return options


if __name__ == "__main__":
    main()
