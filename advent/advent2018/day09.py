import re
from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(9, 2018)


def main():
    lines = advent.get_input_lines()
    players, rounds = list(map(int, re.findall(r"([0-9]+)", lines[0])))

    advent.submit(1, max(play(players, rounds).values()))


def play(players, rounds) -> dict[int, int]:
    scores: dict[int, int] = defaultdict(int)
    player = 0
    circle = [0]
    marble = 1
    current = 0
    while marble < rounds:
        if marble % 23 == 0:
            scores[player] += marble
            to_pop = (current - 7) % len(circle)
            scores[player] += circle.pop(to_pop)
            current = to_pop
        else:
            to_insert = (current + 2) % len(circle)
            if to_insert == 0:
                circle.append(marble)
                current = len(circle) - 1
            else:
                circle.insert(to_insert, marble)
                current = to_insert

        marble += 1
        player = (player + 1) % players

    return scores


if __name__ == "__main__":
    main()
