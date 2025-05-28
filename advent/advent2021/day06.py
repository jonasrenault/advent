from advent.utils import Advent

advent = Advent(6, 2021)


def main():
    lines = advent.get_input_lines()
    fishes = get_fishes(lines[0])
    for _ in range(80):
        fishes = cycle(fishes)
    advent.submit(1, sum(fishes.values()))

    for _ in range(256 - 80):
        fishes = cycle(fishes)
    advent.submit(2, sum(fishes.values()))


def cycle(fishes: dict[int, int]) -> dict[int, int]:
    new_fishes = {8: fishes[0], 6: fishes[0]}
    for t, c in fishes.items():
        if t == 7:
            new_fishes[6] += c
        elif t != 0:
            new_fishes[t - 1] = c
    return new_fishes


def get_fishes(input: str) -> dict[int, int]:
    fishes = {t: 0 for t in range(9)}
    for t in input.split(","):
        fishes[int(t)] += 1
    return fishes


if __name__ == "__main__":
    main()
