from functools import reduce
from math import sqrt
from operator import mul
from typing import cast

import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(8, 2025)


def main():
    lines = advent.get_input_lines()
    points = [
        cast(tuple[int, int, int], tuple(map(int, line.split(",")))) for line in lines
    ]

    distances = euclidean_distances(points)
    circuits, _ = connect(points, distances, 1000)
    circuits.sort(key=lambda x: len(x))
    advent.submit(1, reduce(mul, map(len, circuits[-3:]), 1))

    distances = euclidean_distances(points)
    _, prod = connect(points, distances, None)
    advent.submit(2, prod)


def connect(
    points: list[tuple[int, int, int]],
    distances: npt.NDArray[np.floating],
    limit: int | None,
) -> tuple[list[set[int]], int]:
    max_distance = distances.max()
    distances[distances == 0.0] = max_distance
    circuits = [set([i]) for i in range(len(points))]

    step = 0
    prod = 0
    while len(circuits) > 1 and (limit is None or step < limit):
        a, b = np.unravel_index(distances.argmin(), distances.shape)
        circuits = join(circuits, a, b)  # type: ignore
        distances[a, b] = max_distance
        prod = points[a][0] * points[b][0]
        step += 1

    return circuits, prod


def join(circuits: list[set[int]], a: int, b: int) -> list[set[int]]:
    """
    Join together circuits which contain point a and b

    Args:
        circuits (list[set[int]]): the list of circuits
        a (int): point a's index
        b (int): point b's index

    Returns:
        list[set[int]]: the updated list of circuits
    """
    others = []
    joined = set()
    for circuit in circuits:
        if a in circuit or b in circuit:
            joined |= circuit
        else:
            others.append(circuit)
    return others + [joined]


def euclidean_distances(points: list[tuple[int, int, int]]) -> npt.NDArray[np.floating]:
    """
    Compute the matrix of euclidian distances between points.

    Args:
        points (list[tuple[int, int, int]]): the list of points

    Returns:
        npt.NDArray[np.floating]: the distance matrix.
    """
    nb_points = len(points)
    distances = np.zeros((nb_points, nb_points))
    for i in range(nb_points - 1):
        for j in range(i + 1, nb_points):
            distances[i, j] = distance(points[i], points[j])

    return distances


def distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    x1, y1, z1 = a
    x2, y2, z2 = b
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


if __name__ == "__main__":
    main()
