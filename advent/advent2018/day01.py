from advent.utils.utils import Advent

advent = Advent(1, 2018)


def main():
    lines = advent.get_input_lines()
    advent.submit(1, sum(map(int, lines)))
    advent.submit(2, get_doubles(list(map(int, lines))))


def get_doubles(values: list[int]) -> int:
    sums = set()
    freq = 0
    idx = 0
    while freq not in sums:
        sums.add(freq)
        freq += values[idx % len(values)]
        idx += 1
    return freq


if __name__ == "__main__":
    main()
