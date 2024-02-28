from advent2022.utils.utils import Advent

advent = Advent(2)

HAND_SCORES = {"X": 1, "Y": 2, "Z": 3, "A": 1, "B": 2, "C": 3}

SCORES = {
    ("A", "X"): 3,
    ("B", "Y"): 3,
    ("C", "Z"): 3,
    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("C", "Y"): 0,
    ("A", "Y"): 6,
    ("B", "Z"): 6,
    ("C", "X"): 6,
}

SCORES_2 = {"X": 0, "Y": 3, "Z": 6}

PLAYS = {
    ("A", "X"): "C",
    ("A", "Y"): "A",
    ("A", "Z"): "B",
    ("B", "X"): "A",
    ("B", "Y"): "B",
    ("B", "Z"): "C",
    ("C", "X"): "B",
    ("C", "Y"): "C",
    ("C", "Z"): "A",
}


def main():
    lines = advent.get_input_lines()
    puzzle = [x.strip().split(" ") for x in lines]
    scores = [HAND_SCORES[y] + SCORES[(x, y)] for x, y in puzzle]
    advent.submit(1, sum(scores))

    plays = [HAND_SCORES[PLAYS[x, y]] + SCORES_2[y] for x, y in puzzle]
    advent.submit(2, sum(plays))


if __name__ == "__main__":
    main()
