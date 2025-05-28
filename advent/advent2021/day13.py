import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(13, 2021)


def main():
    lines = advent.get_input_lines()
    paper, folds = get_input(lines)
    paper = fold(paper, folds[0])
    advent.submit(1, np.count_nonzero(paper))

    for f in folds[1:]:
        paper = fold(paper, f)

    strpaper = paper.astype(str)
    strpaper[paper == 0] = "."
    strpaper[paper == 1] = "#"
    for x in range(strpaper.shape[0]):
        print("".join(strpaper[x, :].tolist()))


def fold(paper: npt.NDArray[np.int_], coord: tuple[str, int]) -> npt.NDArray[np.int_]:
    axis, idx = coord
    if axis == "y":
        top = paper[idx:, :]
        bottom = paper[:idx, :]
    else:
        top = paper[:, idx:]
        bottom = paper[:, :idx]
    x, y = np.nonzero(top)
    if axis == "y":
        bottom[idx - x, y] = 1
    else:
        bottom[x, idx - y] = 1
    return bottom


def get_input(lines: list[str]) -> tuple[npt.NDArray[np.int_], list[tuple[str, int]]]:
    points = []
    folds = []
    for line in lines:
        if line and not line.startswith("fold"):
            points.append([int(c) for c in line.split(",")])
        elif line:
            axis, value = line[11:].split("=")
            folds.append((axis, int(value)))

    y, x = np.array(points, dtype=int).max(axis=0)
    paper = np.zeros((x + 1, y + 1), dtype=int)
    for x, y in points:
        paper[y, x] = 1
    return paper, folds


if __name__ == "__main__":
    main()
