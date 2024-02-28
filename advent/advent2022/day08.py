import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(8)


def main():
    lines = advent.get_input_lines()
    trees = np.array([[int(c) for c in line] for line in lines])
    advent.submit(1, int(compute_visible(trees).sum()))
    advent.submit(2, int(np.max(compute_viewing(trees))))


def compute_visible(puzzle: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    For each cell in the matrix, compute whether it is visible from either top, bottom,
    left or right.

    Parameters
    ----------
    puzzle : npt.NDArray[np.int_]
        the input matrix

    Returns
    -------
    npt.NDArray[np.int_]
        a bool np.darray of shape equal to puzzle.
    """
    visible = np.ones(puzzle.shape, dtype=int)
    for i in range(1, puzzle.shape[0] - 1):
        for j in range(1, puzzle.shape[1] - 1):
            left = puzzle[i, :j].max() < puzzle[i, j]
            right = puzzle[i, j + 1 :].max() < puzzle[i, j]
            top = puzzle[:i, j].max() < puzzle[i, j]
            bottom = puzzle[i + 1 :, j].max() < puzzle[i, j]
            visible[i, j] = left or right or top or bottom
    return visible


def compute_viewing(puzzle: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Compute the viewing distance for each cell in the puzzle array.

    Parameters
    ----------
    puzzle : npt.NDArray[np.int_])
        the input array

    Returns
    -------
    npt.NDArray[np.int_])
        an array of shape equal to puzzle's shape and with viewing distances
    """
    viewing = np.zeros(puzzle.shape, dtype=int)
    for i in range(1, puzzle.shape[0] - 1):
        for j in range(1, puzzle.shape[1] - 1):
            left = puzzle[i, :j] >= puzzle[i, j]
            left = 1 + np.argmax(left[::-1]) if np.any(left) else len(left)
            right = puzzle[i, j + 1 :] >= puzzle[i, j]
            right = 1 + np.argmax(right) if np.any(right) else len(right)
            top = puzzle[:i, j] >= puzzle[i, j]
            top = 1 + np.argmax(top[::-1]) if np.any(top) else len(top)
            bottom = puzzle[i + 1 :, j] >= puzzle[i, j]
            bottom = 1 + np.argmax(bottom) if np.any(bottom) else len(bottom)
            viewing[i, j] = left * right * top * bottom
    return viewing


if __name__ == "__main__":
    main()
