from collections import defaultdict
from collections.abc import Iterator

from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(24, 2020)


def main():
    lines = advent.get_input_lines()
    blacks = get_flipped(lines, (0, 0))
    advent.submit(1, len(blacks))

    for _ in tqdm(range(100)):
        blacks = update_day(blacks)
    advent.submit(2, len(blacks))


def update_day(blacks: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Update day pattern, flipping tiles.

    Args:
        blacks (set[tuple[int, int]]): current black tiles

    Returns:
        set[tuple[int, int]]: new set of black tiles
    """
    remove_from_blacks = flip_blacks(blacks)
    add_to_blacks = flip_whites(blacks)
    return (blacks - remove_from_blacks) | add_to_blacks


def flip_blacks(blacks: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Return set of tiles to flip from black to white.

    Args:
        blacks (set[tuple[int, int]]): current black tiles

    Returns:
        set[tuple[int, int]]: set of tiles to flip white
    """
    to_flip = set()
    for tile in blacks:
        tile_neighbors = set(neighbors(tile))
        black_neighbors = tile_neighbors & blacks
        if len(black_neighbors) == 0 or len(black_neighbors) > 2:
            to_flip.add(tile)
    return to_flip


def flip_whites(blacks: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Get set of tiles to flip from white to black.

    Args:
        blacks (set[tuple[int, int]]): current black tiles

    Returns:
        set[tuple[int, int]]: set of tiles to flip black
    """
    white_neighbors = defaultdict(set)
    for tile in blacks:
        for n in neighbors(tile):
            if n not in blacks:
                white_neighbors[n].add(tile)

    to_flip = set()
    for tile, nneighbors in white_neighbors.items():
        if len(nneighbors) == 2:
            to_flip.add(tile)

    return to_flip


def neighbors(tile: tuple[int, int]) -> Iterator[tuple[int, int]]:
    for dir in ("e", "ne", "nw", "w", "sw", "se"):
        yield move_one(tile, dir)


def get_flipped(lines: list[str], start: tuple[int, int]) -> set[tuple[int, int]]:
    """
    Apply all input lines to get set of black tiles.

    Args:
        lines (list[str]): input lines
        start (tuple[int, int]): start tile

    Returns:
        set[tuple[int, int]]: set of black tiles
    """
    blacks: set[tuple[int, int]] = set()
    for instructions in lines:
        tile = move_to(start, instructions)
        if tile in blacks:
            blacks.remove(tile)
        else:
            blacks.add(tile)
    return blacks


def move_to(start: tuple[int, int], instructions: str) -> tuple[int, int]:
    """
    Apply instructions from start node to return end tile coordinates.

    Args:
        start (tuple[int, int]): start tile coordinates
        instructions (str): list of instructions

    Returns:
        tuple[int, int]: end tile coordinates
    """
    curr = start
    for move in moves(instructions):
        curr = move_one(curr, move)
    return curr


def moves(line) -> Iterator[str]:
    """
    Read move instructions.

    Args:
        line (_type_): input line

    Yields:
        Iterator[str]: Iterator of moves
    """
    i = 0
    while i < len(line):
        if line[i] == "s" or line[i] == "n":
            yield line[i : i + 2]
            i += 2
        else:
            yield line[i : i + 1]
            i += 1


def move_one(tile: tuple[int, int], dir: str) -> tuple[int, int]:
    """
    Return coordinates of neighbor tile in given direction.

    Args:
        tile (tuple[int, int]): start tile
        dir (str): direction

    Returns:
        tuple[int, int]: neighbor tile
    """
    x, y = tile
    match dir:
        case "e":
            return (x + 2, y)
        case "ne":
            return (x + 1, y + 1)
        case "nw":
            return (x - 1, y + 1)
        case "w":
            return (x - 2, y)
        case "sw":
            return (x - 1, y - 1)
        case "se":
            return (x + 1, y - 1)
    return x, y


if __name__ == "__main__":
    main()
