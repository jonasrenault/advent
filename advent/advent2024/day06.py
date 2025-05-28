import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(6, 2024)

deltas = ((-1, 0), (0, 1), (1, 0), (0, -1))


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])
    start_position = np.where(grid == "^")
    start = (start_position[0][0], start_position[1][0])

    looped, seen = run(grid, start)
    unique = set([(x, y) for x, y, _ in seen])
    advent.submit(1, len(unique))

    count = 0
    unique.remove(start)
    for position in unique:
        grid[position] = "#"
        looped, _ = run(grid, start)
        count += 1 if looped else 0
        grid[position] = "."

    advent.submit(2, count)


def print_grid(grid: npt.NDArray[np.str_]):
    for row in range(grid.shape[0]):
        print("".join(grid[row]))


def run(
    grid: npt.NDArray[np.str_], start: tuple[int, int]
) -> tuple[bool, set[tuple[int, int, int]]]:
    x, y = start
    dir = 0
    seen: set[tuple[int, int, int]] = set()
    dx, dy = deltas[dir]
    while (
        0 <= x + dx < grid.shape[0]
        and 0 <= y + dy < grid.shape[1]
        and (x, y, dir) not in seen
    ):
        seen.add((x, y, dir))
        dx, dy = deltas[dir]
        if grid[(x + dx, y + dy)] == "#":
            dir = (dir + 1) % 4
        else:
            x, y = x + dx, y + dy
    if (x, y, dir) in seen:
        return True, seen

    seen.add((x, y, dir))
    return False, seen


if __name__ == "__main__":
    main()
