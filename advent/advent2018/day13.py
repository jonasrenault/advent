from functools import cmp_to_key

import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(13, 2018)

DIRS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
ANGLES = {
    "/": {"^": ">", ">": "^", "v": "<", "<": "v"},
    "\\": {"^": "<", ">": "v", "v": ">", "<": "^"},
}
ROTATE_RIGHT = {"^": ">", "<": "^", ">": "v", "v": "<"}
ROTATE_LEFT = {"^": "<", "<": "v", ">": "^", "v": ">"}

CART = tuple[tuple[int, int], str, int]


def main():
    input = advent.get_input()
    grid, carts = read_input(input)
    carts = sorted(carts, key=cmp_to_key(order_carts))

    _, crashes = run(grid, carts)
    crash = crashes.pop()
    print(1, f"{crash[1]},{crash[0]}")

    carts = run_to_last(grid, carts)
    node, dir, rotation = carts[0]
    print(2, f"{node[1]},{node[0]}")


def run_to_last(grid: npt.NDArray[np.str_], carts: list[CART]) -> list[CART]:
    while len(carts) > 1:
        carts, crashes = run(grid, carts)
        carts = [
            (node, dir, rotation) for node, dir, rotation in carts if node not in crashes
        ]
    return carts


def run(
    grid: npt.NDArray[np.str_], carts: list[CART]
) -> tuple[list[CART], set[tuple[int, int]]]:
    crashes: set[tuple[int, int]] = set()
    while not crashes:
        positions = set()
        new_carts = []
        for cart in carts:
            node, dir, rotation = move(grid, *cart)
            if node in positions:
                crashes.add(node)
            positions.add(node)
            new_carts.append((node, dir, rotation))
        carts = sorted(new_carts, key=cmp_to_key(order_carts))
    return carts, crashes


def move(
    grid: npt.NDArray[np.str_], node: tuple[int, int], dir: str, rotation: int
) -> CART:
    if grid[node] in "\\/":
        dir = ANGLES[grid[node]][dir]

    elif grid[node] == "+":
        if rotation == 0:
            dir = ROTATE_LEFT[dir]
            rotation = 1
        elif rotation == 2:
            dir = ROTATE_RIGHT[dir]
            rotation = 0
        else:
            rotation = 2

    x, y = node
    dx, dy = DIRS[dir]
    return (x + dx, y + dy), dir, rotation


def order_carts(c1: CART, c2: CART) -> int:
    (c1x, c1y), _, _ = c1
    (c2x, c2y), _, _ = c2
    if c1x < c2x:
        return -1
    if c1x > c2x:
        return 1
    if c1y < c2y:
        return -1
    if c1y > c2y:
        return 1
    return 0


def read_input(
    input: str,
) -> tuple[npt.NDArray[np.str_], list[CART]]:
    lines = list(input.rstrip("\n").split("\n"))
    grid = np.array([[c for c in line] for line in lines])
    carts = []
    for dir in "^v<>":
        for cart in np.argwhere(grid == dir):
            carts.append((tuple(cart), dir, 0))
            grid[tuple(cart)] = "|" if dir in "^v" else "-"

    return grid, carts


if __name__ == "__main__":
    main()
