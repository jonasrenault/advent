from collections.abc import Callable, Iterator, Sequence
from typing import Any

from advent.utils import Advent, neighbors8

advent = Advent(11, 2020)

deltas_8 = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def main():
    lines = advent.get_input_lines()
    grid = [[c for c in line] for line in lines]
    advent.submit(1, solve(grid, 4, neighbors8))

    lines = advent.get_input_lines()
    grid = [[c for c in line] for line in lines]
    advent.submit(2, solve(grid, 5, neighbors_see))


def solve(
    grid: list[list[str]],
    limit: int,
    neighbors_f: Callable[
        [Sequence[Sequence[Any]], tuple[int, int]], Iterator[tuple[int, int]]
    ],
) -> int:
    """
    Apply changes to grid until no more changes are made and return count of occupied
    seats at the end.

    Args:
        grid (list[list[str]]): the grid
        limit (int): the limit to empty a seat
        neighbors_f (Callable[ [Sequence[Sequence[Any]], tuple[int, int]],
            Iterator[tuple[int, int]] ]): a function returning the
            neighbors for a given seat

    Returns:
        int: the count of occupied seats at the end
    """
    to_fill, to_empty = to_change(grid, limit, neighbors_f)
    while to_fill or to_empty:
        apply_changes(grid, to_fill, to_empty)
        to_fill, to_empty = to_change(grid, limit, neighbors_f)

    count = 0
    for row in grid:
        for seat in row:
            if seat == "#":
                count += 1
    return count


def apply_changes(
    grid: list[list[str]],
    to_fill: list[tuple[int, int]],
    to_empty: list[tuple[int, int]],
):
    for x, y in to_fill:
        grid[x][y] = "#"
    for x, y in to_empty:
        grid[x][y] = "L"


def to_change(
    grid: list[list[str]],
    limit: int,
    neighbors_f: Callable[
        [Sequence[Sequence[Any]], tuple[int, int]], Iterator[tuple[int, int]]
    ],
):
    """
    Given a grid, get the list of seats that should empty of fill.

    Args:
        grid (list[list[str]]): the grid
        limit (int): the limit to empty a seat
        neighbors_f (Callable[ [Sequence[Sequence[Any]], tuple[int, int]],
            Iterator[tuple[int, int]] ]): a function returning
            the neighbors for a given seat

    Returns:
        _type_: _description_
    """
    to_fill = []
    to_empty = []
    for x, row in enumerate(grid):
        for y, seat in enumerate(row):
            if seat == "L":
                if can_fill(grid, (x, y), neighbors_f):
                    to_fill.append((x, y))
            elif seat == "#":
                if must_empty(grid, (x, y), limit, neighbors_f):
                    to_empty.append((x, y))
    return to_fill, to_empty


def must_empty(
    grid: list[list[str]],
    seat: tuple[int, int],
    limit: int,
    neighbors_f: Callable[
        [Sequence[Sequence[Any]], tuple[int, int]], Iterator[tuple[int, int]]
    ],
) -> bool:
    """
    Check if a seat must empty.

    Args:
        grid (list[list[str]]): the grid
        seat (tuple[int, int]): the seat
        limit (int): the limit
        neighbors_f (Callable[ [Sequence[Sequence[Any]], tuple[int, int]],
        Iterator[tuple[int, int]] ]): the neighbors func

    Returns:
        bool: is seat must empty
    """
    fill_count = 0
    for i, j in neighbors_f(grid, seat):
        if grid[i][j] == "#":
            fill_count += 1
            if fill_count >= limit:
                return True
    return False


def can_fill(
    grid: list[list[str]],
    seat: tuple[int, int],
    neighbors_f: Callable[
        [Sequence[Sequence[Any]], tuple[int, int]], Iterator[tuple[int, int]]
    ],
) -> bool:
    """
    Check if seat can fill.

    Args:
        grid (list[list[str]]): the grid
        seat (tuple[int, int]): the seat
        neighbors_f (Callable[ [Sequence[Sequence[Any]], tuple[int, int]],
        Iterator[tuple[int, int]] ]): the neighbors func

    Returns:
        bool: True if seat can fill
    """
    for i, j in neighbors_f(grid, seat):
        if grid[i][j] == "#":
            return False
    return True


def neighbors_see(
    grid: list[list[str]],
    seat: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    return can_see(grid, seat, deltas_8)


def can_see(
    grid: list[list[str]], seat: tuple[int, int], deltas: Sequence[tuple[int, int]]
) -> Iterator[tuple[int, int]]:
    r, c = seat
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dr, dc in deltas:
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            if grid[rr][rc] != ".":
                yield (rr, rc)
            else:
                yield from can_see(grid, (rr, rc), ((dr, dc),))


if __name__ == "__main__":
    main()
