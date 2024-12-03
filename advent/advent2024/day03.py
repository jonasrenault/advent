import re

from advent.utils.utils import Advent

advent = Advent(3, 2024)


def main():
    lines = advent.get_input_lines()
    instructions = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", "".join(lines))
    instructions = [
        (
            int(instruction[4 : instruction.index(",")]),
            int(instruction[instruction.index(",") + 1 : -1]),
        )
        for instruction in instructions
    ]
    advent.submit(1, sum([left * right for left, right in instructions]))

    instructions = re.findall(
        r"(?:mul\([0-9]{1,3},[0-9]{1,3}\)|don't\(\)|do\(\))", "".join(lines)
    )
    active = True
    filtered = []
    for instruction in instructions:
        if instruction == "do()":
            active = True
        elif instruction == "don't()":
            active = False
        elif active:
            filtered.append(
                (
                    int(instruction[4 : instruction.index(",")]),
                    int(instruction[instruction.index(",") + 1 : -1]),
                )
            )
    advent.submit(2, sum([left * right for left, right in filtered]))


if __name__ == "__main__":
    main()
