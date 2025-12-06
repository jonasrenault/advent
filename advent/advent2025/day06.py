import re
from functools import reduce
from operator import mul

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(6, 2025)


def main():
    lines = advent.get_input_lines()
    probs = np.array([re.sub(r"\s+", " ", line).split(" ") for line in lines])

    advent.submit(1, solve(probs))

    input = advent.get_input()
    lines = input.split("\n")[:-1]
    advent.submit(2, solve_vert(lines))


def solve(probs: npt.NDArray[np.str_]) -> int:
    res = []
    for i in range(probs.shape[1]):
        if probs[-1, i] == "+":
            res.append(sum(list(map(int, probs[:-1, i]))))
        else:
            res.append(reduce(mul, list(map(int, probs[:-1, i])), 1))

    return sum(res)


def solve_vert(lines: list[str]) -> int:
    res = []
    operands = lines[:-1]
    operators = lines[-1]
    split_indices = [idx for idx, op in enumerate(operators) if op != " "]
    for i in range(len(split_indices)):
        op_idx = split_indices[i]
        op = operators[op_idx]
        next_op_idx = (
            split_indices[i + 1] - 1 if i < len(split_indices) - 1 else len(operators)
        )
        values = [line[op_idx:next_op_idx] for line in operands]
        vert_values = []
        for j in range(len(values[0])):
            vert_values.append(int("".join([val[j] for val in values])))

        if op == "*":
            res.append(reduce(mul, vert_values, 1))
        else:
            res.append(sum(vert_values))

    return sum(res)


if __name__ == "__main__":
    main()
