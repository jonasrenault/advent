import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(25, 2024)


def main():
    lines = advent.get_input_lines()
    keys, locks = read_input(lines)

    count = 0
    for lock in locks:
        for key in keys:
            valid = all([c1 + c2 <= 5 for c1, c2 in zip(lock, key)])
            if valid:
                count += 1
    advent.submit(1, count)


def read_input(lines: list[str]) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    keys: list[tuple[int, ...]] = []
    locks: list[tuple[int, ...]] = []
    current = []
    for line in lines:
        if line:
            current.append([c for c in line])
        else:
            is_lock, heights = grid_to_heights(np.array(current))
            current = []
            if is_lock:
                locks.append(heights)
            else:
                keys.append(heights)

    is_lock, heights = grid_to_heights(np.array(current))
    if is_lock:
        locks.append(heights)
    else:
        keys.append(heights)

    return keys, locks


def grid_to_heights(item: npt.NDArray[np.str_]) -> tuple[bool, tuple[int, ...]]:
    heights = []
    if item[0, 0] == "#":
        for c in range(item.shape[1]):
            heights.append(max(np.argwhere(item[:, c] == "#"))[0])
        return True, tuple(heights)
    for c in range(item.shape[1]):
        heights.append(5 - max(np.argwhere(item[:, c] == "."))[0])
    return False, tuple(heights)


if __name__ == "__main__":
    main()
