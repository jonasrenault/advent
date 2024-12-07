import re
from itertools import product
from operator import add, mul
from typing import Any

from advent.utils.utils import Advent

advent = Advent(7, 2024)


def main():
    lines = advent.get_input_lines()
    equations = read_equations(lines)
    advent.submit(1, sum([test for test, values in equations if is_valid(test, values)]))

    advent.submit(
        2,
        sum(
            [
                test
                for test, values in equations
                if is_valid(test, values, concatenate=True)
            ]
        ),
    )


def is_valid(test: int, values: tuple[int, ...], concatenate: bool = False) -> bool:
    nb_values = len(values)
    if concatenate:
        operators: tuple[Any, ...] = (add, mul, "||")
    else:
        operators = (add, mul)
    combinations = product(operators, repeat=nb_values - 1)
    for ops in combinations:
        val = values[0]
        for right, op in zip(values[1:], ops):
            if op == "||":
                val = int(str(val) + str(right))
            else:
                val = op(val, right)
        if val == test:
            return True
    return False


def read_equations(lines: list[str]) -> list[tuple[int, tuple[int, ...]]]:
    values = [list(map(int, re.findall(r"([0-9]+)", line))) for line in lines]
    equations = [(v[0], tuple(v[1:])) for v in values]
    return equations


if __name__ == "__main__":
    main()
