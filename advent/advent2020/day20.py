from collections import defaultdict
from collections.abc import Iterator
from itertools import combinations
from math import prod, sqrt

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(20, 2020)


MONSTER = """                  #
#    ##    ##    ###
 #  #  #  #  #  #   """


def main():
    lines = advent.get_input_lines()
    tiles = read_tiles(lines)

    matching_tiles = get_matching_tiles(tiles)
    # corners have only 2 edges
    advent.submit(1, prod([k for k, v in matching_tiles.items() if len(v) == 2]))

    puzzle = build_puzzle(tiles, matching_tiles)

    # trim edges and concatenate tiles
    puzzle = [[c[1:-1, 1:-1] for c in r] for r in puzzle]
    puzzle = [np.concatenate(r, axis=1) for r in puzzle]
    image = np.concatenate(puzzle, axis=0)

    advent.submit(2, find_monsters(MONSTER, image))


def find_monsters(pattern: str, image: npt.NDArray[np.str_]) -> int:
    """
    Find pattern occurences in arrangements of image.

    Args:
        pattern (str): the pattern
        image (npt.NDArray[np.str_]): the image

    Returns:
        int: the water roughness
    """
    # get deltas for # in pattern
    deltas = []
    for x, row in enumerate(pattern.split("\n")):
        for y, c in enumerate(row):
            if c == "#":
                deltas.append((x, y))

    # for each arrangement of image, count matching patterns
    pattern_r = len(pattern.split("\n"))
    pattern_c = len(pattern.split("\n")[0])
    image_r, image_c = image.shape
    monsters = 0
    for r_image in arrangements(image):
        for x in range(image_r - pattern_r):
            for y in range(image_c - pattern_c):
                if all([r_image[x + dx, y + dy] == "#" for dx, dy in deltas]):
                    monsters += 1

        if monsters > 0:
            break

    # count number of # not in patterns
    water_cells = np.count_nonzero(image == "#")
    monster_cells = len(deltas)
    roughness = water_cells - monsters * monster_cells
    return roughness


def build_puzzle(
    tiles: dict[int, npt.NDArray[np.str_]],
    matching_tiles: dict[int, list[int]],
) -> list[list[npt.NDArray[np.str_]]]:
    """
    Build puzzle by placing tiles.

    Args:
        tiles (dict[int, npt.NDArray[np.str_]]): the tiles
        matching_tiles (dict[int, list[int]]): the tiles' matching edges

    Returns:
        list[list[npt.NDArray[np.str_]]]: matrix of rotated tiles
    """
    image_dimension = int(sqrt(len(tiles)))

    # Get and orient top left corner
    top_left_id = [k for k, v in matching_tiles.items() if len(v) == 2].pop()
    top_left = tiles[top_left_id]

    # turn / flip it until its matching edges are to the right and bottom
    matching_edges = set(get_edges(tiles[matching_tiles[top_left_id][0]])) | set(
        get_edges(tiles[matching_tiles[top_left_id][1]])
    )
    while not (
        get_edge(top_left, "R") in matching_edges
        and get_edge(top_left, "B") in matching_edges
    ):
        top_left = np.rot90(top_left)

    to_place = set(tiles.keys()) - {top_left_id}  # set of remaining tiles to place
    first = top_left
    first_id = top_left_id
    image = []
    while to_place:
        row = build_row(first, first_id, tiles, matching_tiles, to_place, image_dimension)
        image.append(row)

        if to_place:  # if we still have tiles to place,
            # match the first tile of the next row to the bottom of the
            # first tile of current row
            first_id, first = match_tile(
                first, first_id, tiles, matching_tiles, to_place, "B", "T"
            )
            to_place.remove(first_id)

    return image


def build_row(
    first: npt.NDArray[np.str_],
    first_id: int,
    tiles: dict[int, npt.NDArray[np.str_]],
    matching_tiles: dict[int, list[int]],
    to_place: set[int],
    image_dimension: int,
) -> list[npt.NDArray[np.str_]]:
    """
    Build a row of dimension image_dimension by adding new tiles to the right of first
    tile.

    Args:
        first (npt.NDArray[np.str_]): the row's positionned first tile
        first_id (int): the row's first tile id
        tiles (dict[int, npt.NDArray[np.str_]]): dict of tiles
        matching_tiles (dict[int, list[int]]): dict of matching tiles
        to_place (set[int]): set of remaining tiles to place
        image_dimension (int): row size

    Returns:
        list[npt.NDArray[np.str_]]: the row of positioned tiles
    """
    prev = first
    prev_id = first_id
    row = [first]
    for _ in range(image_dimension - 1):
        # add a new tile to the right
        tile_id, tile = match_tile(
            prev, prev_id, tiles, matching_tiles, to_place, "R", "L"
        )
        # remove added tile from available tiles
        to_place.remove(tile_id)
        row.append(tile)
        prev = tile
        prev_id = tile_id

    return row


def match_tile(
    tile: npt.NDArray[np.str_],
    tile_id: int,
    tiles: dict[int, npt.NDArray[np.str_]],
    matching_tiles: dict[int, list[int]],
    to_place: set[int],
    edge_a: str,
    edge_b: str,
) -> tuple[int, npt.NDArray[np.str_]]:
    """
    Given a positionned tile A, find another tile B in tile A's matching tiles and rotate
    / flip it such that tile A and tile B match on edge_a and edge_b.

    Args:
        tile (npt.NDArray[np.str_]): first tile
        tile_id (int): first tile id
        tiles (dict[int, npt.NDArray[np.str_]]): dict of tiles
        matching_tiles (dict[int, list[int]]): dict of matching tiles
        to_place (set[int]): set of remaining tiles to place
        edge_a (str): matching edge for tile A
        edge_b (str): matching edge for tile B

    Returns:
        tuple[int, npt.NDArray[np.str_]]: matching tile id and tile
    """
    # get first tile's edge
    side_a = get_edge(tile, edge_a)

    # get set of possible matching tiles
    other_tiles = set(matching_tiles[tile_id]) & to_place

    # iterate over all possible matching tiles
    for other_id in other_tiles:
        other = tiles[other_id]
        # Arrange second tile in any possible way
        for other in arrangements(other):
            # Until the two sides match
            if side_a == get_edge(other, edge_b):
                return other_id, other
    return -1, np.zeros((1, 1), dtype=str)


def get_matching_tiles(tiles: dict[int, npt.NDArray[np.str_]]) -> dict[int, list[int]]:
    """
    Find tiles with matching edges.

    Args:
        tiles (dict[int, npt.NDArray[np.str_]]): dict of tile_id -> tile

    Returns:
        dict[int, list[int]]: dict of tile_id -> list of matching tile ids
    """
    matching_tiles = defaultdict(list)
    for p1, p2 in tqdm(combinations(tiles.keys(), 2)):
        ep1 = get_edges(tiles[p1])
        ep2 = get_edges(tiles[p2])
        if ep1 & ep2:
            matching_tiles[p1].append(p2)
            matching_tiles[p2].append(p1)

    return matching_tiles


def get_edges(tile: npt.NDArray[np.str_]) -> set[str]:
    """
    Get all possible edges for a tile by rotating and fliping it.

    Args:
        tile (npt.NDArray[np.str_]): the tile

    Returns:
        set[str]: set of all possible edges
    """
    return set([np.array2string(r[0, :]) for r in arrangements(tile)])


def arrangements(tile: npt.NDArray[np.str_]) -> Iterator[npt.NDArray[np.str_]]:
    """
    Rotate and flip tile to build all possible arrangements of a tile.

    Args:
        tile (npt.NDArray[np.str_]): the tile

    Yields:
        Iterator[npt.NDArray[np.str_]]: iterator of possible arrangements
    """
    for _ in range(2):
        for _ in range(4):
            tile = np.rot90(tile)
            yield tile
        tile = np.flip(tile, 1)


def get_edge(tile: npt.NDArray[np.str_], edge: str) -> str:
    """
    Get top, bottom, left or right edge of a tile.

    Args:
        tile (npt.NDArray[np.str_]): the tile
        edge (str): the edge

    Returns:
        str: the tile's edge
    """
    if edge == "T":
        return np.array2string(tile[0, :])
    if edge == "L":
        return np.array2string(tile[:, 0])
    if edge == "R":
        return np.array2string(tile[:, -1])
    return np.array2string(tile[-1, :])


def read_tiles(lines: list[str]) -> dict[int, npt.NDArray[np.str_]]:
    """
    Read tiles into a dict of tile_id -> tile.

    Args:
        lines (list[str]): input lines

    Returns:
        dict[int, npt.NDArray[np.str_]]: dict of tiles
    """
    id = -1
    arr = []
    tiles = {}
    for line in lines:
        if line.startswith("Tile"):
            id = int(line[5:-1])
        elif line:
            arr.append([c for c in line])
        else:
            tiles[id] = np.array(arr, dtype=str)
            arr = []
    tiles[id] = np.array(arr, dtype=str)
    return tiles


if __name__ == "__main__":
    main()
