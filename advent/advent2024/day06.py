import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(6, 2024)

deltas = ((-1, 0), (0, 1), (1, 0), (0, -1))


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    start = np.where(grid == "^")

    seen = run(grid, (start[0][0], start[1][0]))
    advent.submit(1, len(seen))


def print_grid(grid: npt.NDArray[np.str_]):
    for row in range(grid.shape[0]):
        print("".join(grid[row]))


def run(grid: npt.NDArray[np.str_], start: tuple[int, int]) -> set[tuple[int, int]]:
    x, y = start
    dir = 0
    seen: set[tuple[int, int]] = set()
    seen.add((x, y))
    dx, dy = deltas[dir]
    while 0 <= x + dx < grid.shape[0] and 0 <= y + dy < grid.shape[1]:
        dx, dy = deltas[dir]
        if grid[(x + dx, y + dy)] == "#":
            dir = (dir + 1) % 4
        else:
            x, y = x + dx, y + dy
            seen.add((x, y))
    return seen


if __name__ == "__main__":
    main()
