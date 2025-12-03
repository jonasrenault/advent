from operator import itemgetter

from advent.utils import Advent

advent = Advent(3, 2025)


def main():
    lines = advent.get_input_lines()

    advent.submit(1, sum([joltage(bank, 2) for bank in lines]))
    advent.submit(2, sum([joltage(bank, 12) for bank in lines]))


def joltage(bank: str, size: int) -> int:
    values = []
    start = 0
    for k in range(size):
        to_search = bank[start : (-size + k + 1)] if size > k + 1 else bank[start:]
        max_index, max_value = max(enumerate(to_search), key=itemgetter(1))
        values.append(max_value)
        start = start + max_index + 1
    return int("".join(values))


if __name__ == "__main__":
    main()
