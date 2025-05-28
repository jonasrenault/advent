from advent.utils import Advent

advent = Advent(2, 2021)


def main():
    lines = advent.get_input_lines()
    forward = sum([int(line[8:]) for line in lines if line.startswith("forward")])
    up = sum([int(line[3:]) for line in lines if line.startswith("up")])
    down = sum([int(line[5:]) for line in lines if line.startswith("down")])
    advent.submit(1, forward * (down - up))

    advent.submit(2, forward * get_depth(lines))


def get_depth(lines: list[str]) -> int:
    aim, depth = 0, 0
    for line in lines:
        if line.startswith("down"):
            aim += int(line[len("down") + 1 :])
        elif line.startswith("up"):
            aim -= int(line[3:])
        else:
            depth += int(line[len("forward") + 1 :]) * aim
    return depth


if __name__ == "__main__":
    main()
