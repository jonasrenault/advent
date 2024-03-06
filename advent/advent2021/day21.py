from collections.abc import Iterator

from advent.utils.utils import Advent

advent = Advent(21, 2021)


def main():
    lines = advent.get_input_lines()
    p1 = int(lines[0][-1])
    p2 = int(lines[1][-1])
    rolls, scores = play(p1, p2)
    advent.submit(1, rolls * min(scores.values()))


def play(p1: int, p2: int) -> tuple[int, dict[int, int]]:
    rolls = 0
    positions = {0: p1, 1: p2}
    scores = {0: 0, 1: 0}
    dice = get_dice()
    turn = 0
    while scores[0] < 1000 and scores[1] < 1000:
        move = sum([next(dice) for _ in range(3)])
        positions[turn] = 1 + ((positions[turn] - 1 + move) % 10)
        scores[turn] += positions[turn]
        turn = (turn + 1) % 2
        rolls += 3
    return rolls, scores


def get_dice() -> Iterator[int]:
    d = 1
    while True:
        yield d
        d = 1 + (d % 100)


if __name__ == "__main__":
    main()
