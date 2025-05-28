from collections import defaultdict
from collections.abc import Iterator
from functools import lru_cache
from itertools import product

from advent.utils import Advent

advent = Advent(21, 2021)


def main():
    lines = advent.get_input_lines()
    p1 = int(lines[0][-1])
    p2 = int(lines[1][-1])
    rolls, scores = play(p1, p2)
    advent.submit(1, rolls * min(scores.values()))

    p1w, p2w = play_dirac(0, (p1, p2), (0, 0))
    advent.submit(2, max(p1w, p2w))


@lru_cache(maxsize=None)
def play_dirac(
    turn: int, positions: tuple[int, int], scores: tuple[int, int]
) -> tuple[int, int]:
    if scores[0] >= 21:
        return 1, 0
    if scores[1] >= 21:
        return 0, 1

    p1wins = 0
    p2wins = 0
    for weight, state in next_states(turn, positions, scores):
        left, right = play_dirac(*state)
        p1wins += left * weight
        p2wins += right * weight

    return p1wins, p2wins


def next_states(turn: int, positions: tuple[int, int], scores: tuple[int, int]):
    rolls = list(product((1, 2, 3), repeat=3))
    moves: dict[int, int] = defaultdict(int)
    for roll in rolls:
        moves[sum(roll)] += 1

    states = []

    new_turn = (turn + 1) % 2
    for move, weight in moves.items():
        new_positions = tuple(
            [
                1 + ((p - 1 + move) % 10) if i == turn else p
                for i, p in enumerate(positions)
            ]
        )
        new_scores = tuple(
            [s + new_positions[i] if i == turn else s for i, s in enumerate(scores)]
        )
        states.append((weight, (new_turn, new_positions, new_scores)))

    return states


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
