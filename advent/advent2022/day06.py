from advent2022.utils.utils import Advent

advent = Advent(6)


def main():
    lines = advent.get_input_lines()
    advent.submit(1, find_header(lines[0], 4))
    advent.submit(2, find_header(lines[0], 14))


def find_header(buffer: str, unique: int) -> int:
    for i in range(unique, len(buffer)):
        if len(set(buffer[i - unique : i])) == unique:
            return i
    return -1


if __name__ == "__main__":
    main()
