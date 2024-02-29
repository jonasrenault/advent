from advent.utils.utils import Advent

advent = Advent(1, 2023)

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def calibration(lines: list[str]) -> int:
    calibrations = [tuple(c for c in line if c.isdigit()) for line in lines]
    calibration = [int(c[0] + c[-1]) for c in calibrations]
    return sum(calibration)


def main():
    lines = advent.get_input_lines()
    advent.submit(1, calibration(lines))

    input = advent.get_input()
    for k, v in DIGITS.items():
        input = input.replace(k, k + v + k)
    lines = list(map(lambda line: line.strip(), input.rstrip("\n").split("\n")))
    advent.submit(2, calibration(lines))


if __name__ == "__main__":
    main()
