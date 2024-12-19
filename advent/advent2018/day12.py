from advent.utils.utils import Advent

advent = Advent(12, 2018)


def main():
    lines = advent.get_input_lines()
    state, patterns = read_input(lines)

    _, score = run(state, patterns)
    advent.submit(1, score)


def run(state: str, patterns: dict[str, str]) -> tuple[int, int]:
    offset = 3
    state = "." * offset + state + "." * offset
    print(str(0).zfill(2), state)
    for i in range(1, 21):
        state, offset = apply(state, patterns, offset)
        print(str(i).zfill(2), state, len(state))

    return offset, sum([i - offset for i in range(len(state)) if state[i] == "#"])


def apply(state: str, patterns: dict[str, str], offset: int) -> tuple[str, int]:
    new_state = (
        state[:2]
        + "".join(
            [patterns.get(state[i - 2 : i + 3], ".") for i in range(2, len(state) - 2)]
        )
        + state[-2:]
    )

    if "#" in new_state[-5:]:
        new_state += "." * 5

    if "#" in new_state[:2]:
        new_state = "." * 2 + new_state
        offset += 2

    return new_state, offset


def read_input(lines: list[str]) -> tuple[str, dict[str, str]]:
    state = lines[0][lines[0].index(":") + 2 :]
    patterns = dict()
    for line in lines[2:]:
        pattern, result = line.split(" => ")
        patterns[pattern] = result

    return state, patterns


if __name__ == "__main__":
    main()
