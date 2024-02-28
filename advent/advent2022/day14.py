import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(14)


def main():
    lines = advent.get_input_lines()
    cave = get_cave(lines)
    advent.submit(1, fill_cave(cave))

    advent.submit(2, fill_cave_floored(cave))


def fill_cave_floored(cave: npt.NDArray[np.int_]) -> int:
    bottom = np.argwhere(cave == 1)[:, 0].max()
    c = cave.copy()
    c[bottom + 2, :] = 1
    res = drop_sand_unit(c, bottom)
    cnt = 0
    while res is not None and res != (500, 0):
        x, y = res
        c[y, x] = 2
        cnt += 1
        res = drop_sand_unit(c, bottom)
    return cnt + 1


def fill_cave(cave: npt.NDArray[np.int_]) -> int:
    bottom = np.argwhere(cave == 1)[:, 0].max()
    c = cave.copy()
    res = drop_sand_unit(c, bottom)
    cnt = 0
    while res is not None:
        x, y = res
        c[y, x] = 2
        cnt += 1
        res = drop_sand_unit(c, bottom)
    return cnt


def drop_sand_unit(cave: npt.NDArray[np.int_], bottom: int) -> tuple[int, int] | None:
    rest = False
    x, y = 500, 0
    while not rest:
        # find lowest stopping point vertically
        low = np.argwhere(cave[y:, x] > 0)
        if low.size == 0:
            # we're falling into the abyss, break and exit
            return None

        y = low.min() - 1 + y
        # try to drop left diag
        if cave[y + 1, x - 1] == 0 and y <= bottom:
            y += 1
            x -= 1
        # try to drop right diag
        elif cave[y + 1, x + 1] == 0 and y <= bottom:
            y += 1
            x += 1
        # we stop
        else:
            rest = True
    return x, y


def get_cave(lines: list[str]) -> npt.NDArray[np.int_]:
    cave = np.zeros((1000, 1000), dtype=int)
    for line in lines:
        coords = line.split(" -> ")
        x0 = -1
        y0 = -1
        for coord in coords:
            y, x = map(int, coord.split(","))
            if x == x0:
                cave[x, min(y0, y) : max(y0, y) + 1] = 1
            elif y == y0:
                cave[min(x0, x) : max(x0, x) + 1, y] = 1
            x0 = x
            y0 = y
    return cave


if __name__ == "__main__":
    main()
