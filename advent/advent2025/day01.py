from advent.utils import Advent

advent = Advent(1, 2025)


def main():
    lines = advent.get_input_lines()

    curr = 50
    stops, total = 0, 0
    for line in lines:
        curr, counts = rotate(curr, line)
        total += counts
        if curr == 0:
            stops += 1

    advent.submit(1, stops)
    advent.submit(2, total)


def rotate(start: int, rotation: str) -> tuple[int, int]:
    dir = rotation[0]
    val = int(rotation[1:])

    if dir == "R":
        pos = start + val
    else:
        pos = start - val

    end = pos % 100
    counts = abs(pos // 100)
    # handle special cases when going left
    if start == 0 and dir == "L":
        counts -= 1
    if end == 0 and dir == "L":
        counts += 1
    return pos % 100, counts


if __name__ == "__main__":
    main()
