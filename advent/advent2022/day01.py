from advent2022.utils.utils import Advent

advent = Advent(1)


def main():
    lines = advent.get_input_lines()
    elves = get_elves(lines)
    advent.submit(1, max(map(sum, elves)))

    elves.sort(key=lambda elf: sum(elf))
    advent.submit(2, sum(map(sum, elves[-3:])))


def get_elves(lines: list[str]) -> list[tuple[int, ...]]:
    elves = []
    elf = []
    for line in lines:
        if line:
            elf.append(int(line))
        else:
            elves.append(tuple(elf))
            elf = []
    elves.append(tuple(elf))
    return elves


if __name__ == "__main__":
    main()
