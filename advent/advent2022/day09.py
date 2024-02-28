import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(9)

dirs = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def main():
    lines = advent.get_input_lines()
    cmds: list[tuple[str, str]] = [tuple(line.split()) for line in lines]
    positions = run(cmds)
    advent.submit(1, len(positions))

    advent.submit(2, len(run_knots(cmds)))


def run_knots(cmds: list[tuple[str, str]]) -> set[tuple[int, int]]:
    knots = [np.array((0, 0)) for _ in range(10)]
    positions = set()
    positions.add((0, 0))
    for s in cmds:
        step_knots(knots, s, positions)

    return positions


def step_knots(
    knots: list[npt.NDArray[np.int_]],
    s: tuple[str, str],
    positions: set[tuple[int, int]],
):
    d, u = s
    for _ in range(int(u)):
        # move head in dir
        knots[0] = knots[0] + np.array(dirs[d])
        moved = True
        i = 1
        while moved and i < 10:
            # for each knot, move it in direction of knot before it
            # if it is not touching it
            diff = knots[i - 1] - knots[i]
            if diff.max() > 1 or diff.min() < -1:
                knots[i] = knots[i] + diff.clip(-1, 1)
                i += 1
            else:
                moved = False
            if i == 10:
                positions.add(tuple(knots[i - 1]))


def run(cmds: list[tuple[str, str]]) -> set[tuple[int, int]]:
    H = (0, 0)
    T = (0, 0)
    positions = set()
    positions.add((0, 0))
    for s in cmds:
        H, T = step(H, T, s, positions)

    return positions


def step(
    H: tuple[int, int],
    T: tuple[int, int],
    s: tuple[str, str],
    positions: set[tuple[int, int]],
):
    d, u = s
    for _ in range(int(u)):
        new_H = (H[0] + dirs[d][0], H[1] + dirs[d][1])
        if abs(new_H[0] - T[0]) > 1 or abs(new_H[1] - T[1]) > 1:
            T = H
            positions.add(T)
        H = new_H
    return H, T


if __name__ == "__main__":
    main()
