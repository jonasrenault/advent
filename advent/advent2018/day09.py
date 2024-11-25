import re
from collections import defaultdict, deque

from advent.utils.utils import Advent

advent = Advent(9, 2018)


def main():
    lines = advent.get_input_lines()
    nb_players, max_marble = list(map(int, re.findall(r"([0-9]+)", lines[0])))

    advent.submit(1, max(play(nb_players, max_marble).values()))
    advent.submit(2, max(play(nb_players, max_marble * 100).values()))


def play(nb_players: int, max_marble: int) -> dict[int, int]:
    scores: dict[int, int] = defaultdict(int)
    circle = deque([0])
    for marble in range(1, max_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % nb_players] += circle.pop() + marble
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return scores


if __name__ == "__main__":
    main()
