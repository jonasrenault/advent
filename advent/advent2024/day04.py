import numpy as np
import numpy.typing as npt

from advent.utils.algos import deltas_8
from advent.utils import Advent

advent = Advent(4, 2024)

XMAS = "XMAS"
deltas_x = (
    (-1, -1),
    (1, 1),
)

deltas_x_2 = (
    (-1, 1),
    (1, -1),
)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    advent.submit(1, count_xmas(grid))

    advent.submit(2, count_mas(grid))


def count_mas(grid: npt.NDArray[np.str_]) -> int:
    count = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[(r, c)] == "A":
                count += count_mas_for_pos(grid, (r, c))
    return count


def count_mas_for_pos(grid: npt.NDArray[np.str_], node: tuple[int, int]) -> int:
    r, c = node
    for diag in (deltas_x, deltas_x_2):
        letters = {"S", "M"}
        for dr, dc in diag:
            rr, rc = r + dr, c + dc
            if (
                0 <= rr < grid.shape[0]
                and 0 <= rc < grid.shape[1]
                and grid[rr, rc] in letters
            ):
                letters.remove(grid[rr, rc])
            else:
                return 0
    return 1


def count_xmas(grid: npt.NDArray[np.str_]) -> int:
    count = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[(r, c)] == "X":
                count += count_xmas_for_pos(grid, (r, c))
    return count


def count_xmas_for_pos(grid: npt.NDArray[np.str_], node: tuple[int, int]) -> int:
    count = 0
    for dr, dc in deltas_8:
        r, c = node
        for letter in XMAS[1:]:
            r, c = r + dr, c + dc
            if not (
                0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == letter
            ):
                break
        else:
            count += 1
    return count


if __name__ == "__main__":
    main()
