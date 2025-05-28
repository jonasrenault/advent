from itertools import product

import numpy as np
from tqdm import tqdm

from advent.utils import Advent

advent = Advent(17, 2020)

neighbors3d = list(product([0, 1, -1], repeat=3))[1:]
neighbors4d = list(product([0, 1, -1], repeat=4))[1:]


def main():
    lines = advent.get_input_lines()
    space = np.array([[[c for c in line] for line in lines]], dtype=str)
    for _ in tqdm(range(6)):
        space = expand(space)
        to_active, to_inactive = cycle(space)
        for node in to_active:
            space[node] = "#"
        for node in to_inactive:
            space[node] = "."

    advent.submit(1, len(np.where(space == "#")[0]))

    space4d = np.array([[[[c for c in line] for line in lines]]], dtype=str)
    for _ in tqdm(range(6)):
        space4d = expand4d(space4d)
        to_active, to_inactive = cycle4d(space4d)
        for node in to_active:
            space4d[node] = "#"
        for node in to_inactive:
            space4d[node] = "."
    advent.submit(2, len(np.where(space4d == "#")[0]))


def cycle4d(space):
    sw, sz, sx, sy = space.shape
    to_active = []
    to_inactive = []
    for w in range(sw):
        for z in range(sz):
            for x in range(sx):
                for y in range(sy):
                    cube = space[w, z, x, y]
                    an = active_n_4d(space, (w, z, x, y))
                    if cube == "#" and an not in (2, 3):
                        to_inactive.append((w, z, x, y))
                    elif cube == "." and an == 3:
                        to_active.append((w, z, x, y))

    return to_active, to_inactive


def cycle(space):
    sz, sx, sy = space.shape
    to_active = []
    to_inactive = []
    for z in range(sz):
        for x in range(sx):
            for y in range(sy):
                cube = space[z, x, y]
                an = active_n_3d(space, (z, x, y))
                if cube == "#" and an not in (2, 3):
                    to_inactive.append((z, x, y))
                elif cube == "." and an == 3:
                    to_active.append((z, x, y))

    return to_active, to_inactive


def expand(space):
    sz, sx, sy = space.shape
    new = np.full((sz + 2, sx + 2, sy + 2), ".", dtype=str)
    new[1:-1, 1:-1, 1:-1] = space
    return new


def expand4d(space):
    sw, sz, sx, sy = space.shape
    new = np.full((sw + 2, sz + 2, sx + 2, sy + 2), ".", dtype=str)
    new[1:-1, 1:-1, 1:-1, 1:-1] = space
    return new


def active_n_3d(space, node):
    sz, sx, sy = space.shape
    z, x, y = node
    c = 0
    for dz, dx, dy in neighbors3d:
        if 0 <= z + dz < sz and 0 <= x + dx < sx and 0 <= y + dy < sy:
            if space[z + dz, x + dx, y + dy] == "#":
                c += 1
    return c


def active_n_4d(space, node):
    sw, sz, sx, sy = space.shape
    w, z, x, y = node
    c = 0
    for dw, dz, dx, dy in neighbors4d:
        if (
            0 <= w + dw < sw
            and 0 <= z + dz < sz
            and 0 <= x + dx < sx
            and 0 <= y + dy < sy
        ):
            if space[w + dw, z + dz, x + dx, y + dy] == "#":
                c += 1
    return c


if __name__ == "__main__":
    main()
