from typing import cast

import numpy as np
import numpy.typing as npt
from numpy.lib.stride_tricks import sliding_window_view

from advent.utils.utils import Advent

advent = Advent(11, 2018)


def main():
    lines = advent.get_input_lines()
    serial = int(lines[0])

    powers = np.array(
        [[power(x, y, serial) for y in range(1, 301)] for x in range(1, 301)]
    )

    max3, _ = get_max_block_coords(powers, 3)
    advent.submit(1, f"{max3[0] + 1},{max3[1] + 1}")

    max_val = 0
    max_id = (0, 0, 0)
    for window in range(1, 300):
        coords, val = get_max_block_coords(powers, window)
        if val > max_val:
            max_val = val
            max_id = (coords[0] + 1, coords[1] + 1, window)
    advent.submit(2, f"{max_id[0]},{max_id[1]},{max_id[2]}")


def get_max_block_coords(
    powers: npt.NDArray[np.int_], window_size: int
) -> tuple[tuple[int, int], int]:
    blocks = sliding_window_view(powers, (window_size, window_size))
    sums: npt.NDArray[np.int_] = np.sum(blocks, axis=(2, 3))
    coords = cast(tuple[int, int], np.unravel_index(np.argmax(sums), sums.shape))
    return coords, sums[coords]


def power(x: int, y: int, serial: int) -> int:
    level = (((x + 10) * y) + serial) * (x + 10)
    if level < 100:
        return -5
    return int(str(level)[-3]) - 5


if __name__ == "__main__":
    main()
