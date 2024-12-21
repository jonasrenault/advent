import heapq
import math
from itertools import product
from typing import Iterator

import numpy as np
import numpy.typing as npt

from advent.utils.utils import Advent

advent = Advent(21, 2024)
DIR = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}


def main():
    lines = advent.get_input_lines()
    numeric = np.array(
        [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]
    )
    directional = np.array([["#", "^", "A"], ["<", "v", ">"]])

    complexities = {}
    for code in lines:
        complexities[code] = len(find_user_sequence(code, numeric, directional)[0])
        print(code, complexities[code])
    # complexities = {
    #     code: len(find_user_sequence(code, numeric, directional)[0]) for code in lines
    # }
    advent.submit(1, sum([int(code[:-1]) * val for code, val in complexities.items()]))


def find_user_sequence(
    code: str, numeric: npt.NDArray[np.str_], directional: npt.NDArray[np.str_]
) -> list[list[str]]:
    seqs1 = find_sequence(
        numeric,
        code,
    )
    seqs2 = []
    for seq1 in seqs1:
        seqs2.extend(find_sequence(directional, "".join(seq1)))
    minl = min([len(s) for s in seqs2])
    seqs2 = [s for s in seqs2 if len(s) == minl]

    seqs3 = []
    for seq2 in seqs2:
        seqs3.extend(find_sequence(directional, "".join(seq2)))
    minl = min([len(s) for s in seqs3])
    seqs3 = [s for s in seqs3 if len(s) == minl]
    return seqs3


def find_sequence(keypad: npt.NDArray[np.str_], input: str) -> list[list[str]]:
    res: list[list[str]] = []
    start = tuple(np.argwhere(keypad == "A")[0])
    for target in input:
        _, paths = find_paths(keypad, start, target)
        if not res:
            res = [path + ["A"] for path in paths]
        else:
            res = [res + path + ["A"] for res, path in product(res, paths)]
        start = tuple(np.argwhere(keypad == target)[0])
    return res


def neighbors(
    grid: npt.NDArray[np.str_], node: tuple[int, int]
) -> Iterator[tuple[str, tuple[int, int]]]:
    r, c = node
    maxr = len(grid) - 1
    maxc = len(grid[0]) - 1
    for dir, (dr, dc) in DIR.items():
        rr, rc = r + dr, c + dc
        if 0 <= rr <= maxr and 0 <= rc <= maxc:
            yield dir, (rr, rc)


def find_paths(
    grid: npt.NDArray[np.str_],
    start: tuple[int, int],
    target: str,
) -> tuple[float, list[list[str]]]:
    distance = {start: 0}
    best_distance = math.inf
    best_paths: list[list[str]] = []
    queue: list[tuple[int, tuple[int, int], list[str]]] = [(0, start, [])]

    while queue:
        dist, node, path = heapq.heappop(queue)
        if grid[node] == target:
            if dist < best_distance:
                best_distance = dist
                best_paths = [path]
            elif dist == best_distance:
                best_paths.append(path)
            continue

        if node in distance and distance[node] < dist:
            continue

        distance[node] = dist

        for dir, neighbor in neighbors(grid, node):
            if grid[neighbor] != "#":
                new_dist = dist + 1
                heapq.heappush(queue, (new_dist, neighbor, path + [dir]))

    return best_distance, best_paths


if __name__ == "__main__":
    main()
