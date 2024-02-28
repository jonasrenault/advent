import string
from itertools import batched

from advent2022.utils.utils import Advent

advent = Advent(3)


def main():
    lines = advent.get_input_lines()
    commons = [
        set(line[: len(line) // 2]) & set(line[len(line) // 2 :]) for line in lines
    ]
    priorities = map(lambda s: string.ascii_letters.index(s.pop()) + 1, commons)
    advent.submit(1, sum(priorities))

    teams = [set(x) & set(y) & set(z) for x, y, z in batched(lines, 3)]
    priorities = map(lambda s: string.ascii_letters.index(s.pop()) + 1, teams)
    advent.submit(2, sum(priorities))


if __name__ == "__main__":
    main()
