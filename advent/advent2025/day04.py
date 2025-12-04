import numpy as np
import numpy.typing as npt

from advent.utils import Advent
from advent.utils.algos import neighbors8

advent = Advent(4, 2025)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    rolls = np.argwhere(grid == "@")
    count = 0
    for roll in rolls:
        nrolls = [n for n in neighbors8(grid, roll) if grid[n] == "@"]  # type: ignore
        if len(nrolls) < 4:
            count += 1

    advent.submit(1, count)
    advent.submit(2, clear(grid))


def clear(grid: npt.NDArray[np.str_]) -> int:
    removed = True
    while removed:
        removed = False
        rolls = np.argwhere(grid == "@")
        for roll in rolls:
            nrolls = [n for n in neighbors8(grid, roll) if grid[n] == "@"]  # type: ignore
            if len(nrolls) < 4:
                grid[*roll] = "x"
                removed = True

    total = len(np.where(grid == "x")[0])
    return total


if __name__ == "__main__":
    main()
