import math
import re

from advent.utils import Advent

advent = Advent(2, 2023)

game_max = {"red": 12, "green": 13, "blue": 14}


def is_game_impossible(draws: list[str]):
    for d in draws:
        for c in d.split(","):
            s = re.match(r"\s*(\d+) (\w+)\s*", c)
            if s is not None:
                count = int(s.group(1))
                color = s.group(2)
                if count > game_max[color]:
                    return True
    return False


def min_possible_count(draws: list[str]):
    counts = {"red": 0, "green": 0, "blue": 0}
    for d in draws:
        for c in d.split(","):
            s = re.match(r"\s*(\d+) (\w+)\s*", c)
            if s is not None:
                count = int(s.group(1))
                color = s.group(2)
                if counts[color] < count:
                    counts[color] = count
    return counts


def main():
    games = advent.get_input_lines()
    impossible_count = 0
    for game in games:
        id = re.search(r"Game (\d+)", game).group(1)
        if id is not None:
            draws = game[game.index(":") + 1 :].split(";")
            if not is_game_impossible(draws):
                impossible_count += int(id)

    advent.submit(1, impossible_count)

    power_sum = 0
    for game in games:
        draws = game[game.index(":") + 1 :].split(";")
        counts = min_possible_count(draws)
        power = math.prod(counts.values())
        power_sum += power

    advent.submit(2, power_sum)


if __name__ == "__main__":
    main()
