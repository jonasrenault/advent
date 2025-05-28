from collections import defaultdict

from advent.utils import Advent

advent = Advent(1, 2024)


def main():
    lines = advent.get_input_lines()
    pairs = [tuple(map(int, line.split())) for line in lines]
    left = sorted([lh for lh, _ in pairs])
    right = sorted([r for _, r in pairs])
    advent.submit(1, sum([abs(lh - rh) for lh, rh in zip(left, right)]))

    right_counts = defaultdict(int)
    for value in right:
        right_counts[value] += 1

    advent.submit(2, sum([value * right_counts[value] for value in left]))


if __name__ == "__main__":
    main()
