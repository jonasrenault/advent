import re
from collections import defaultdict

from advent2022.utils.utils import Advent

advent = Advent(5)


def main():
    input = advent.get_input()
    lines = input.rstrip("\n").split("\n")

    piles, moves = read_input(lines)
    apply_moves(piles, moves, True)
    tops = [piles[i + 1][0] for i in range(max(piles.keys()))]
    advent.submit(1, "".join(tops))

    piles, moves = read_input(lines)
    apply_moves(piles, moves, False)
    tops = [piles[i + 1][0] for i in range(max(piles.keys()))]
    advent.submit(2, "".join(tops))


def apply_moves(
    piles: dict[int, list[str]], moves: list[tuple[int, int, int]], reversed: bool
):
    for qty, fr, to in moves:
        moved = piles[fr][:qty]
        if reversed:
            moved = moved[::-1]
        piles[to] = moved + piles[to]
        piles[fr] = piles[fr][qty:]


def read_input(
    lines: list[str],
) -> tuple[dict[int, list[str]], list[tuple[int, int, int]]]:
    piles = defaultdict(list)
    moves = []
    for line in lines:
        if not line:
            continue
        if "[" in line:
            for i in range(1, len(line), 4):
                if line[i] != " ":
                    piles[(i // 4) + 1].append(line[i])
        if line.startswith("move"):
            m = re.match(r"move (\d+) from (\d+) to (\d+)", line)
            if m is not None:
                (qty, fr, to) = int(m.group(1)), int(m.group(2)), int(m.group(3))
                moves.append((qty, fr, to))

    return piles, moves


if __name__ == "__main__":
    main()
