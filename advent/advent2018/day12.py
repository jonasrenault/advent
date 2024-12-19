from advent.utils.utils import Advent

advent = Advent(12, 2018)


def main():
    lines = advent.get_input_lines()
    state, patterns = read_input(lines)

    offset = 3
    state = "." * offset + state + "." * offset
    state, offset = run(state, patterns, offset, 20)
    advent.submit(1, score(state, offset))

    target = 50000000000
    step, s, diff = find_loop(state, patterns, offset)
    advent.submit(2, s + diff * (target - step))


def find_loop(state: str, patterns: dict[str, str], offset) -> tuple[int, int, int]:
    step = 100
    state1, offset = run(state, patterns, offset, step - 2)
    state2, offset = run(state1, patterns, offset, 1)
    state3, offset = run(state2, patterns, offset, 1)

    while score(state2, offset) - score(state1, offset) != score(state3, offset) - score(
        state2, offset
    ):
        state1 = state2
        state2 = state3
        state3, offset = run(state2, patterns, offset, 1)
        step += 1

    return step, score(state3, offset), score(state3, offset) - score(state2, offset)


def score(state: str, offset: int) -> int:
    return sum([i - offset for i in range(len(state)) if state[i] == "#"])


def run(state: str, patterns: dict[str, str], offset: int, steps: int) -> tuple[str, int]:
    for _ in range(steps):
        state, offset = apply(state, patterns, offset)
    return state, offset


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
