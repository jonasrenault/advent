import numpy as np
import numpy.typing as npt

from advent.utils import Advent

advent = Advent(7, 2025)


def main():
    lines = advent.get_input_lines()
    grid = np.array([[c for c in line] for line in lines])

    splits, timelines = beam(grid)

    advent.submit(1, splits)
    advent.submit(2, timelines)


def beam(grid: npt.NDArray[np.str_]) -> tuple[int, int]:
    rays = np.array(grid[0, :] == "S", dtype=int)
    splits = 0
    for row in range(1, grid.shape[1]):
        splitters = grid[row, :] == "^"
        active_splitters = np.nonzero(splitters & rays.astype(bool))[0]
        splits += len(active_splitters)
        for split in active_splitters:
            timelines = rays[split]
            rays[split] = 0
            if split > 0:
                rays[split - 1] += timelines
            if split < len(rays) - 1:
                rays[split + 1] += timelines

    return splits, rays.sum().item()


if __name__ == "__main__":
    main()
