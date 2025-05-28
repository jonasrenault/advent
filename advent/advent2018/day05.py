from advent.utils import Advent

advent = Advent(5, 2018)


def main():
    lines = advent.get_input_lines()
    polymer = lines[0]
    advent.submit(1, react(polymer))

    advent.submit(
        2,
        min(
            [
                react(polymer.replace(x.lower(), "").replace(x.upper(), ""))
                for x in set(polymer)
            ]
        ),
    )


def are_opposite(left: str, right: str) -> bool:
    return left.lower() == right.lower() and (
        (left.isupper() and right.islower()) or (left.islower() and right.isupper())
    )


def react(polymer: str) -> int:
    buffer: list[str] = []
    for c in polymer:
        if buffer and are_opposite(c, buffer[-1]):
            buffer.pop()
        else:
            buffer.append(c)
    return len(buffer)


if __name__ == "__main__":
    main()
