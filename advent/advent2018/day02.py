from collections import Counter
from itertools import combinations

from advent.utils.utils import Advent

advent = Advent(2, 2018)


def main():
    lines = advent.get_input_lines()
    counts = [Counter(line) for line in lines]
    twos = sum([1 for c in counts if 2 in c.values()])
    threes = sum([1 for c in counts if 3 in c.values()])
    advent.submit(1, twos * threes)

    for b1, b2 in combinations(lines, 2):
        common = [left for left, right in zip(b1, b2) if left == right]
        if len(common) == len(b1) - 1:
            advent.submit(2, "".join(common))
            break


if __name__ == "__main__":
    main()
