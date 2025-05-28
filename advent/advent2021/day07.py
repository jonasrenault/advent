from advent.utils import Advent

advent = Advent(7, 2021)


def main():
    lines = advent.get_input_lines()
    pos = list(map(int, lines[0].split(",")))
    diffs = [sum([abs(x - p) for x in pos]) for p in range(max(pos))]
    advent.submit(1, min(diffs))

    diffs2 = [
        sum([abs(x - p) * (abs(x - p) + 1) / 2 for x in pos]) for p in range(max(pos))
    ]
    advent.submit(2, int(min(diffs2)))


if __name__ == "__main__":
    main()
