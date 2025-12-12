from collections.abc import Sequence
from itertools import combinations_with_replacement
from typing import Any, TypeAlias, cast

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent.utils import Advent

advent = Advent(12, 2025)

Tree: TypeAlias = tuple[int, int]
Shape: TypeAlias = npt.NDArray[np.int_]
Kernel: TypeAlias = tuple[npt.NDArray[np.int_], ...]


def main():
    lines = advent.get_input_lines()
    shapes, trees, presents = read_input(lines)

    total = 0
    for tree, counts in tqdm(zip(trees, presents)):
        if solve(shapes, tree, counts):
            total += 1

    print(1, total)


def solve(shapes: list[Shape], tree: Tree, presents: list[int]) -> bool:
    # Sanity check, ensure there is enough free space to fit all presents
    free = tree[0] * tree[1]
    required = sum(
        [np.count_nonzero(shapes[idx]) * count for idx, count in enumerate(presents)]
    )
    if required < free:
        return False

    return True

    # present_shapes = [
    #     (count, shapes[idx]) for idx, count in enumerate(presents) if count > 0
    # ]
    # grid = np.zeros(tree)

    # for _ in fits(grid, present_shapes):
    #     return True

    # return False


def fits(grid: npt.NDArray[np.int_], presents: list[tuple[int, Shape]]):
    if len(presents) == 0:
        yield grid

    for pidx in range(len(presents)):
        count, shape = presents[pidx]
        for combination in combinations_with_replacement(kernels(shape), count):
            for new_grid in fill(grid, shape.shape, combination):
                yield from fits(new_grid, slice(presents, pidx))


def fill(
    grid: npt.NDArray[np.int_], kernel_shape: tuple[int, int], kernels: Sequence[Kernel]
):
    if len(kernels) == 0:
        yield grid

    free_space = np.count_nonzero(grid == 0)
    if free_space > kernel_shape[0] * kernel_shape[1] * len(kernels):

        for x in range(grid.shape[0] - kernel_shape[0] + 1):
            for y in range(grid.shape[1] - kernel_shape[1] + 1):
                for ki in range(len(kernels)):
                    kx, ky = kernels[ki]
                    if not grid[kx + x, ky + y].any():
                        new_grid = grid.copy()
                        new_grid[kx + x, ky + y] = 1
                        yield from fill(new_grid, kernel_shape, slice(kernels, ki))


def kernels(shape: Shape) -> list[Kernel]:
    return [
        np.nonzero(shape),
        np.nonzero(np.rot90(shape)),
        np.nonzero(np.rot90(shape, 2)),
        np.nonzero(np.rot90(shape, 3)),
    ]


def slice(kernels: Sequence[Any], index: int) -> list[Any]:
    return [k for i, k in enumerate(kernels) if i != index]


def read_input(lines: list[str]):
    shapes: list[npt.NDArray[np.int_]] = []
    shape: list[list[int]] = []
    trees = []
    presents = []
    for line in lines:
        if "x" in line:
            trees.append(
                cast(tuple[int, int], tuple(map(int, line[: line.index(":")].split("x"))))
            )
            presents.append(list(map(int, line[line.index(":") + 2 :].split())))
        elif ":" in line:
            shape = []
        elif "." in line or "#" in line:
            shape.append([1 if c == "#" else 0 for c in line])
        else:
            shapes.append(np.array(shape))
    return shapes, trees, presents


if __name__ == "__main__":
    main()
