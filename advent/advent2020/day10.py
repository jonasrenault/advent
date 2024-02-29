from functools import lru_cache
from math import prod

from advent.utils.utils import Advent

advent = Advent(10, 2020)


def main():
    lines = advent.get_input_lines()
    lines = [int(x) for x in lines]
    adapters = lines + [3 + max(lines)]
    adapters.sort()
    advent.submit(1, prod(diff([0] + adapters).values()))
    advent.submit(2, search(0, tuple(adapters)))


@lru_cache
def search(joltage, adapters: tuple[int, ...]) -> int:
    """
    Find possible combinations for adapters.

    Args:
        joltage (_type_): the current joltage
        adapters (tuple[int, ...]): the sorted list of available adapters

    Returns:
        int: the number of combinations
    """
    if len(adapters) == 1:
        return 1

    sum = 0
    for i, x in enumerate(adapters):
        if x - joltage <= 3:
            sum += search(x, adapters[i + 1 :])
        else:
            break
    return sum


def diff(adapters: list[int]) -> dict[int, int]:
    """
    Count number of 1 or 3 diffs in list of adapters.

    Args:
        adapters (list[int]): sorted list of adapters

    Returns:
        dict[int, int]: dict of counts
    """
    res = {1: 0, 3: 0}
    for i in range(len(adapters) - 1):
        res[adapters[i + 1] - adapters[i]] += 1
    return res


if __name__ == "__main__":
    main()
