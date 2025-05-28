import re

import numpy as np

from advent.utils import Advent

advent = Advent(3, 2018)


def main():
    lines = advent.get_input_lines()
    fabric = np.zeros((2000, 2000), dtype=int)
    for line in lines:
        _, left, top, width, height = tuple(map(int, re.findall(r"-?\d+", line)))
        fabric[top + 1 : top + height + 1, left + 1 : left + width + 1] += 1
    advent.submit(1, np.count_nonzero(fabric > 1))

    for line in lines:
        id, left, top, width, height = tuple(map(int, re.findall(r"-?\d+", line)))
        if np.all(fabric[top + 1 : top + height + 1, left + 1 : left + width + 1] == 1):
            advent.submit(2, id)
            break


if __name__ == "__main__":
    main()
