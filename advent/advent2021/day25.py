from advent.utils.utils import Advent

advent = Advent(25, 2021)

DELTAS = {">": (0, 1), "v": (1, 0)}


def main():
    lines = advent.get_input_lines()
    (max_r, max_c), cucumbers = get_cucumbers(lines)

    advent.submit(1, moves(max_r, max_c, cucumbers))


def moves(max_r: int, max_c: int, cucumbers: dict[tuple[int, int], str]) -> int:
    moved = 1
    step = 0
    while moved:
        move_east = move_herd(max_r, max_c, cucumbers, ">")
        move_south = move_herd(max_r, max_c, cucumbers, "v")
        moved = move_east + move_south
        step += 1
    return step


def move_herd(
    max_r: int, max_c: int, cucumbers: dict[tuple[int, int], str], herd: str
) -> int:
    to_move = set()
    for (r, c), dir in cucumbers.items():
        if dir == herd:
            rr, rc = neighbor(max_r, max_c, r, c, dir)
            if (rr, rc) not in cucumbers:
                to_move.add((r, c))

    for r, c in to_move:
        cucumbers[neighbor(max_r, max_c, r, c, herd)] = herd
        del cucumbers[(r, c)]

    return len(to_move)


def neighbor(max_r: int, max_c: int, r: int, c: int, dir: str) -> tuple[int, int]:
    dr, dc = DELTAS[dir]
    rr = r + dr
    rc = c + dc
    if rr >= max_r:
        return (0, rc)
    if rc >= max_c:
        return (rr, 0)
    return (rr, rc)


def get_cucumbers(lines: list[str]) -> tuple[tuple[int, int], dict[tuple[int, int], str]]:
    max_r = len(lines)
    max_c = len(lines[0])
    cucumbers: dict[tuple[int, int], str] = dict()
    for r, row in enumerate(lines):
        for c, col in enumerate(row):
            if col != ".":
                cucumbers[(r, c)] = col
    return (max_r, max_c), cucumbers


if __name__ == "__main__":
    main()
