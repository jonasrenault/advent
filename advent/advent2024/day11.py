import functools

from advent.utils import Advent

advent = Advent(11, 2024)


def main():
    lines = advent.get_input_lines()
    stones = list(map(int, lines[0].split()))
    advent.submit(1, sum([count(stone, 25) for stone in stones]))
    advent.submit(2, sum([count(stone, 75) for stone in stones]))


@functools.lru_cache(maxsize=None)
def count(stone: int, step: int) -> int:
    if step == 0:
        return 1

    if stone == 0:
        return count(1, step - 1)
    if len(str(stone)) % 2 == 0:
        length = len(str(stone))
        return count(int(str(stone)[: length // 2]), step - 1) + count(
            int(str(stone)[length // 2 :]), step - 1
        )
    return count(stone * 2024, step - 1)


if __name__ == "__main__":
    main()
