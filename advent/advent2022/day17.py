from collections.abc import Iterator
from itertools import cycle

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent2022.utils.utils import Advent

advent = Advent(17)


STONES = [
    np.array(((0, 0), (0, 1), (0, 2), (0, 3))),
    np.array(((0, 1), (-1, 0), (-1, 1), (-1, 2), (-2, 1))),
    np.array(((0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2))),
    np.array(((0, 0), (-1, 0), (-2, 0), (-3, 0))),
    np.array(((0, 0), (0, 1), (-1, 0), (-1, 1))),
]


def main():
    lines = advent.get_input_lines()
    jets = lines[0]
    cave = simulate(jets, 2022)
    advent.submit(1, height_of_cave(cave))
    advent.submit(2, simulate_with_pattern(jets, 1000000000000))


def get_mask(
    cave: npt.NDArray[np.int_], mask_size: int
) -> tuple[int, tuple[tuple[int, ...], ...]] | None:
    """
    Given a cave and a mask_size, return the mask_size topmost rows in the cave.

    Parameters
    ----------
    cave : npt.NDArray[np.int_]
        The cave
    mask_size : int
        The mask_size

    Returns
    -------
    tuple[tuple[int]]
        A tuple of tuple containing the mask_size highest rows in the cave
    """
    top = np.argwhere(cave == 1)
    if not top:
        return None

    height = cave.shape[0] - top[:, 0].min()
    if height <= mask_size:
        return None

    return height, tuple(tuple(x) for x in cave[top : top + mask_size, :])


def simulate_with_pattern(jets: str, n_rocks: int, mask_size: int = 30) -> int:
    """
    Simulate droping `n_rocks` rocks. This method keeps a history of what the topmost rows
    in the cave looked like after droping each rock, to look for repeatable patterns.

    Parameters
    ----------
    n_rocks : int
        the number of rocks to drop
    mask_size : int
        the mask_size to use

    Returns
    -------
    int
        the height of the cave after droping all the rocks
    """
    history: dict[tuple[int, str, tuple[tuple[int, ...], ...]], tuple[int, int]] = {}
    t = 0
    cave = np.zeros((10000, 7), dtype=int)
    gjets = cycle(jets)
    pattern_height = 0

    while t < n_rocks:
        stone = STONES[t % 5]
        jet = drop_stone(stone, cave, gjets)
        mask_height = get_mask(cave, mask_size)
        if mask_height is not None:
            height, mask = mask_height
            key = (t % 5, jet, mask)
            if key in history:
                # we found a pattern. Multiply height and time of
                # pattern as many times as needed to reach goal.
                last_time, last_height = history[key]
                tdiff = t - last_time
                n_repeats = (n_rocks - t) // tdiff
                pattern_height += (height - last_height) * n_repeats
                t += tdiff * n_repeats
                history = {}
            else:
                history[key] = (t, height)
        t += 1

    return height + pattern_height


def height_of_cave(cave: npt.NDArray[np.int_]) -> int:
    if len(np.argwhere(cave == 1)) == 0:
        return 0
    return cave.shape[0] - np.argwhere(cave == 1)[:, 0].min()


def simulate(jets: str, n_rocks: int) -> npt.NDArray[np.int_]:
    cave = np.zeros((10000, 7), dtype=int)
    gjets = cycle(jets)
    for i in tqdm(range(n_rocks)):
        stone = STONES[i % 5]
        drop_stone(stone, cave, gjets)
    return cave


def push_stone(
    stone: npt.NDArray[np.int_],
    cave: npt.NDArray[np.int_],
    jet: str,
    bl: npt.NDArray[np.int_],
) -> npt.NDArray[np.int_]:
    """
    Given a stone, a cave, a jet direction and the bottom left position of the stone, move
    it in the given direction if possible.

    Parameters
    ----------
    stone : npt.NDArray[np.int_]
        the stone shape
    cave : npt.NDArray[np.int_]
        the cave array
    jet : str
        the jet direction
    bl : npt.NDArray[np.int_]
        the bottom left position for the stone shape

    Returns
    -------
    npt.NDArray[np.int_]]
        the moved bottom left position
    """
    dir = (0, 1) if jet == ">" else (0, -1)
    pos = stone + bl + dir
    if pos[:, 1].max() > 6 or pos[:, 1].min() < 0 or np.any(cave[tuple(pos.T)] == 1):
        return bl
    return bl + dir


def fall_stone(
    stone: npt.NDArray[np.int_], cave: npt.NDArray[np.int_], bl: npt.NDArray[np.int_]
) -> tuple[bool, npt.NDArray[np.int_]]:
    """
    Move a stone down.

    Parameters
    ----------
    stone : npt.NDArray[np.int_]
        the stone shape
    cave : npt.NDArray[np.int_]
        the cave
    bl : npt.NDArray[np.int_]
        the bottom left position for the stone

    Returns
    -------
    tuple[bool, npt.NDArray[np.int_]]
        whether the stone moved, and its updated position
    """
    pos = stone + bl + (1, 0)
    if bl[0] == cave.shape[0] - 1 or np.any(cave[tuple(pos.T)] == 1):
        return True, bl
    return False, bl + (1, 0)


def drop_stone(
    stone: npt.NDArray[np.int_], cave: npt.NDArray[np.int_], ijets: Iterator[str]
):
    """
    Drop a stone in the cave.

    Parameters
    ----------
    stone : np.ndarray
        The stone shape
    cave : np.ndarray
        The cave
    ijets : Iterator[str]
        An iterator for the jet streams
    """
    high_point = (
        cave.shape[0] if len(cave[cave == 1]) == 0 else np.argwhere(cave == 1)[:, 0].min()
    )
    bl = np.array((high_point - 4, 2))
    rest = False
    while not rest:
        jet = next(ijets)
        bl = push_stone(stone, cave, jet, bl)
        rest, bl = fall_stone(stone, cave, bl)
        if rest:
            cave[tuple((bl + stone).T)] = 1

    return jet


if __name__ == "__main__":
    main()
