from collections.abc import Iterable
from functools import lru_cache
from math import inf

from advent.utils.algos import deltas_4
from advent.utils.utils import Advent

advent = Advent(23, 2021)

ROOMS = {"A": 3, "B": 5, "C": 7, "D": 9}
ENTRANCES = ((1, 3), (1, 5), (1, 7), (1, 9))
ENERGIES = {"A": 1, "B": 10, "C": 100, "D": 1000}


def main():
    lines = advent.get_input()
    grid = [[c for c in line] for line in lines.strip("\n").split("\n")]
    pods = get_pods(grid)
    spaces = free_space(grid)
    advent.submit(1, solve(tuple(spaces), tuple(pods)))


@lru_cache(maxsize=None)
def solve(spaces: tuple[tuple[int, int]], pods: tuple[tuple[str, int, int]]) -> float:
    if finished(pods):
        return 0

    best = inf
    for p, r, c in pods:
        for rr, rc, cost in next_moves(spaces, pods, p, r, c):
            next_state = update_pods(pods, p, r, c, rr, rc)
            cost += solve(spaces, next_state)  # type: ignore

            if cost < best:
                best = cost

    return best


def update_pods(
    pods: Iterable[tuple[str, int, int]], p: str, r: int, c: int, rr: int, rc: int
) -> tuple[tuple[str, int, int], ...]:
    return tuple(
        [
            (px, pr, pc) if (px, pr, pc) != (p, r, c) else (p, rr, rc)
            for px, pr, pc in pods
        ]
    )


def finished(pods: Iterable[tuple[str, int, int]]) -> bool:
    for p, r in ROOMS.items():
        pods_in_r = pods_in_room(pods, r)
        if len(pods_in_r) < 2 or not all([p == x for x in pods_in_r]):
            return False
    return True


def print_grid(
    grid: list[list[str]], pods: set[tuple[str, int, int]], spaces: set[tuple[int, int]]
):
    pod_coords = {(r, c): p for p, r, c in pods}
    for r, row in enumerate(grid):
        p = ""
        for c, col in enumerate(row):
            if (r, c) in spaces:
                if (r, c) in pod_coords:
                    p += pod_coords[(r, c)]
                else:
                    p += "."
            else:
                p += col
        print(p)


def next_moves(
    spaces, pods: Iterable[tuple[str, int, int]], pod: str, r: int, c: int
) -> set[tuple[int, int, int]]:
    moves: set[tuple[int, int, int]] = set()
    # don't leave own room unless there is another pod in same room
    if r > 1 and c == ROOMS[pod]:
        otherpods_in_r = set(pods_in_room(pods, c)) - set([pod])
        if len(otherpods_in_r) == 0:
            return moves

    # first get all possible moves
    pod_positions = {(r, c) for _, r, c in pods}
    energy = ENERGIES[pod]
    distances = {(r, c): 0}
    queue = [(0, (r, c))]

    while queue:
        dist, (nr, nc) = queue.pop()
        for dr, dc in deltas_4:
            rr, rc = nr + dr, nc + dc
            if (rr, rc) in spaces and (rr, rc) not in pod_positions:
                new_dist = dist + energy
                if (rr, rc) not in distances or new_dist < distances[(rr, rc)]:
                    distances[(rr, rc)] = new_dist
                    queue.append((new_dist, (rr, rc)))

    # then filter these moves
    for (rr, rc), v in distances.items():
        if (rr, rc) == (r, c):
            # don't stay in same place
            continue
        if (rr, rc) in ENTRANCES:
            # don't stop in entrances
            continue
        if r > 1 and rr > 1:
            # you can only move from room to hallway
            continue
        if r == 1 and rr == 1:
            # You can only move from hallway to a room
            continue
        if (
            r == 1 and rr > 1
        ):  # don't leave hallway unless its to go in own room with same pods
            room = ROOMS[pod]
            otherpods_in_r = set(pods_in_room(pods, ROOMS[pod])) - set([pod])
            if rc != room or len(otherpods_in_r) > 0:
                continue
            if (
                rr == 2 and (3, rc) not in pod_positions
            ):  # If entering an empty room, move to the back
                continue
            return {(rr, rc, v)}

        if finished(update_pods(pods, pod, r, c, rr, rc)):
            # if one move finishes, return this only
            return {(rr, rc, v)}

        moves.add((rr, rc, v))
    return moves


def pods_in_room(pods: Iterable[tuple[str, int, int]], room: int) -> list[str]:
    return [p for p, r, c in pods if c == room and r > 1]


def free_space(grid: list[list[str]]) -> set[tuple[int, int]]:
    spaces = set()
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col in "ABCD.":
                spaces.add((r, c))
    return spaces


def get_pods(grid: list[list[str]]) -> set[tuple[str, int, int]]:
    pods = set()
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col in "ABCD":
                pods.add((col, r, c))
    return pods


def get_grid(lines: str):
    grid = [[c for c in line] for line in lines.strip("\n").split("\n")]
    return grid


if __name__ == "__main__":
    main()
