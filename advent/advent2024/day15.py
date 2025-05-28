from operator import itemgetter

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(15, 2024)

DIR = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines if line.startswith("#")])
    directions = "".join(
        [line for line in lines if line.startswith(("^", "<", ">", "v"))]
    )

    run(grid, directions)
    advent.submit(1, score(grid))

    grid2 = np.array(
        [
            [
                c
                for c in line.replace("#", "##")
                .replace("O", "[]")
                .replace(".", "..")
                .replace("@", "@.")
            ]
            for line in lines
            if line.startswith("#")
        ]
    )

    run(grid2, directions)
    advent.submit(2, score(grid2, "["))


def run(grid: npt.NDArray[np.str_], directions: str):
    """
    Run all movements from directions on grid

    Args:
        grid (npt.NDArray[np.str_]): the grid.
        directions (str): string of directions
    """
    robot = tuple(np.argwhere(grid == "@")[0])

    for dir in directions:
        moved = move(grid, robot, dir)
        if moved:
            robot = tuple(np.add(robot, DIR[dir]))


def print_grid(grid: npt.NDArray[np.str_]):
    """
    Print a grid.

    Args:
        grid (npt.NDArray[np.str_]): grid to print.
    """
    for row in grid:
        print("".join(row))


def score(grid: npt.NDArray[np.str_], target: str = "O") -> int:
    """
    Return grid's score

    Args:
        grid (npt.NDArray[np.str_]): the grid.
        target (str, optional): target to score, either O or [. Defaults to "O".

    Returns:
        int: the score
    """
    return sum([100 * x + y for x, y in zip(*np.where(grid == target))])


def to_move(
    grid: npt.NDArray[np.str_], node: tuple[int, int], dir: str
) -> set[tuple[int, int]]:
    """
    Return set of nodes to move together

    Args:
        grid (npt.NDArray[np.str_]): the grid.
        node (tuple[int, int]): current node to move
        dir (str): direction of movement

    Returns:
        set[tuple[int, int]]: set of nodes to move together.
    """
    x, y = node
    dx, dy = DIR[dir]

    nodes = set((node,))
    if grid[node] in "[]" and dir in ("^v"):
        other_node = (x, y - 1) if grid[node] == "]" else (x, y + 1)
        nodes.add(other_node)

    res = set(nodes)
    for x, y in nodes:
        neighbor = (x + dx, y + dy)
        if not (grid[neighbor] == "." or grid[neighbor] == "#"):
            res |= to_move(grid, neighbor, dir)

    return res


def can_move(grid: npt.NDArray[np.str_], nodes: set[tuple[int, int]], dir: str) -> bool:
    """
    Check if a set a nodes can move in given direction.

    Args:
        grid (npt.NDArray[np.str_]): the grid.
        nodes (set[tuple[int, int]]): set of nodes to move.
        dir (str): the direction

    Returns:
        bool: whether the nodes can move or not.
    """
    dx, dy = DIR[dir]
    for x, y in nodes:
        neighbor = (x + dx, y + dy)
        if not (neighbor in nodes or grid[neighbor] == "."):
            return False
    return True


def move_nodes(grid: npt.NDArray[np.str_], nodes: set[tuple[int, int]], dir: str):
    """
    Move a set of nodes in given direction

    Args:
        grid (npt.NDArray[np.str_]): the grid
        nodes (set[tuple[int, int]]): set of nodes to move
        dir (str): the direction
    """
    dx, dy = DIR[dir]
    sorted_nodes = list(nodes)
    sorted_nodes.sort(
        key=itemgetter(1) if dir in "<>" else itemgetter(0), reverse=dir in ">v"
    )
    for x, y in sorted_nodes:
        grid[(x + dx, y + dy)] = grid[(x, y)]
        grid[(x, y)] = "."


def move(grid: npt.NDArray[np.str_], node: tuple[int, int], dir: str) -> bool:
    """
    Move the given node and all boxes in given direction.

    Args:
        grid (npt.NDArray[np.str_]): the grid.
        node (tuple[int, int]): the node to move.
        dir (str): the direction

    Returns:
        bool: Whether tne node moved or not.
    """
    nodes = to_move(grid, node, dir)
    moved = can_move(grid, nodes, dir)
    if moved:
        move_nodes(grid, nodes, dir)
    return moved


if __name__ == "__main__":
    main()
