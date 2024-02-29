from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(9, 2020)


def main():
    lines = advent.get_input_lines()
    lines = [int(x) for x in lines]
    val = find_invalid(lines)
    advent.submit(1, val)

    r = find_range(val, lines)
    advent.submit(2, min(r) + max(r))


def find_invalid(lines: list[int]):
    for i, x in tqdm(enumerate(lines[25:])):
        if not is_valid(x, lines[i : 25 + i]):
            return x
    return -1


def is_valid(number: int, previous: list[int]):
    for i, x in enumerate(previous):
        for y in previous[i + 1 :]:
            if x + y == number:
                return True
    return False


def find_range(target: int, lines: list[int]) -> list[int]:
    for line in range(2, len(lines)):
        for i in range(len(lines) - line):
            if sum(lines[i : i + line]) == target:
                return lines[i : i + line]
    return []


if __name__ == "__main__":
    main()
