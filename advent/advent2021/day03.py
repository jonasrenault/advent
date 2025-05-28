import operator
from collections.abc import Callable

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(3, 2021)


def main():
    lines = advent.get_input_lines()
    nums = np.array([[int(c) for c in line] for line in lines], dtype=int)
    avg = np.mean(nums, axis=0)
    gamma = np.array(avg > 0.5, dtype=int)
    epsilon = np.array(avg < 0.5, dtype=int)

    advent.submit(
        1, int("".join(map(str, gamma)), base=2) * int("".join(map(str, epsilon)), base=2)
    )

    oxygen = rating(nums, operator.ge)
    co2 = rating(nums, operator.lt)
    advent.submit(
        2,
        int("".join(map(str, oxygen[0])), base=2)
        * int("".join(map(str, co2[0])), base=2),
    )


def rating(inputs: npt.NDArray[np.int_], op: Callable[[float, float], bool]):
    col = 0
    while len(inputs) > 1:
        if op(np.mean(inputs[:, col]), 0.5):
            inputs = inputs[inputs[:, col] == 1, :]
        else:
            inputs = inputs[inputs[:, col] == 0, :]
        col += 1
    return inputs


if __name__ == "__main__":
    main()
