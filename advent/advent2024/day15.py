import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(15, 2024)

DIR = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines if line.startswith("#")])
    directions = "".join(
        [line for line in lines if line.startswith(("^", "<", ">", "v"))]
    )

    robot = tuple(np.argwhere(grid == "@")[0])

    for dir in directions:
        moved = move(grid, robot, dir)
        if moved:
            robot = tuple(np.add(robot, DIR[dir]))

    advent.submit(1, score(grid))


def score(grid: npt.NDArray[np.str_]) -> int:
    return sum([100 * x + y for x, y in zip(*np.where(grid == "O"))])


def move(grid: npt.NDArray[np.str_], node: tuple[int, int], dir: str) -> bool:
    dx, dy = DIR[dir]
    x, y = node
    moved = False
    if grid[(x + dx, y + dy)] == ".":
        moved = True
    elif grid[(x + dx, y + dy)] == "#":
        moved = False
    else:
        moved = move(grid, (x + dx, y + dy), dir)

    if moved:
        grid[(x + dx, y + dy)] = grid[node]
        grid[node] = "."

    return moved


if __name__ == "__main__":
    main()
