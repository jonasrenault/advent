from advent2022.utils.utils import Advent

advent = Advent(4)


def main():
    lines = advent.get_input_lines()
    pairs = get_pairs(lines)
    overlaps = [p for p in pairs if overlap(p)]
    advent.submit(1, len(overlaps))

    touches = [p for p in pairs if touch(p)]
    advent.submit(2, len(touches))


def overlap(pairs: tuple[tuple[int, ...], tuple[int, ...]]) -> bool:
    (a1, b1), (a2, b2) = pairs
    return a1 >= a2 and b1 <= b2 or a1 <= a2 and b1 >= b2


def touch(pairs: tuple[tuple[int, ...], tuple[int, ...]]) -> bool:
    (a1, b1), (a2, b2) = pairs
    return min(b1, b2) - max(a1, a2) >= 0


def get_pairs(lines: list[str]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    pairs = []
    for line in lines:
        h, t = line.split(",")
        p1 = map(int, h.split("-"))
        p2 = map(int, t.split("-"))
        pairs.append((tuple(p1), tuple(p2)))
    return pairs


if __name__ == "__main__":
    main()
