from collections import deque

from advent.utils.utils import Advent

advent = Advent(24, 2021)


def main():
    lines = advent.get_input_lines()
    constants = get_constants(lines)

    number = get_max_number(constants)
    advent.submit(1, number)


def get_max_number(constants: list[tuple[int, int]]) -> int:
    constraints = []
    stack: deque[tuple[int, int]] = deque()
    for i, (a, b) in enumerate(constants):
        if a > 0:
            stack.append((i, b))
        else:
            j, b = stack.pop()
            constraints.append((i, j, a + b))

    digits = [0] * 14
    for i, j, diff in constraints:
        if diff > 0:
            digits[i], digits[j] = 9, 9 - diff
        else:
            digits[i], digits[j] = 9 + diff, 9

    num = 0
    for d in digits:
        num = num * 10 + d
    return num


def get_constants(lines: list[str]) -> list[tuple[int, int]]:
    constants = []
    for i in range(5, len(lines), 18):
        constants.append((int(lines[i][6:]), int(lines[i + 10][6:])))
    return constants


if __name__ == "__main__":
    main()
