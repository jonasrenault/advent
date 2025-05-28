from math import ceil, floor

from advent.utils import Advent

advent = Advent(5, 2020)


def main():
    lines = advent.get_input_lines()
    rows = [find(128, line[:7], "F") for line in lines]
    cols = [find(8, line[7:], "L") for line in lines]
    ids = [r * 8 + c for r, c in zip(rows, cols)]
    advent.submit(1, max(ids))

    s = None
    for i in range(max(ids)):
        if i not in ids and i - 1 in ids and i + 1 in ids:
            s = i
            break
    advent.submit(2, s)


def find(r: int, input: str, lower: str) -> int:
    s = 0
    e = r - 1
    for i in input:
        if e - s == 1:
            if i == lower:
                return s
            return e
        if i == lower:
            e = s + floor((e - s) / 2)
        else:
            s = s + ceil((e - s) / 2)
    return -1


if __name__ == "__main__":
    main()
