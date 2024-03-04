from advent.utils.utils import Advent

advent = Advent(8, 2021)


digits = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


def main():
    lines = advent.get_input_lines()
    outputs = [line.split("|")[1].split() for line in lines]
    counts = [len([x for x in output if len(x) in (2, 3, 4, 7)]) for output in outputs]
    advent.submit(1, sum(counts))

    values = [get_ouput(line) for line in lines]
    advent.submit(2, sum(values))


def get_ouput(line: str) -> int:
    """
    Given an input line, guess the mapping from the input, then use it to find out the
    output value.

    Parameters
    ----------
    line : str
        input puzzle line

    Returns
    -------
    int
        the output value
    """

    input, output = line.split(" | ")
    mapping = map_input(input.split())

    value = ""
    for digit in output.split():
        for k, v in mapping.items():
            if set(v) == set(digit):
                value += str(k)

    return int(value)


def map_input(input: list[str]) -> dict[int, str]:
    """
    Given a list of possible values for all ten digits, guess which value corresponds to
    which digit by comparing common values in mappings.

    Parameters
    ----------
    input : list[str]
        the input digit values

    Returns
    -------
    dict[int, str]
        the guessed mapping for each digit
    """
    mapping: dict[int, str] = dict()
    i = 0
    while len(mapping) < 10:
        digit = input[i]
        if digit not in mapping.values():
            candidates = {
                k: digit
                for k, v in digits.items()
                if len(v) == len(digit) and k not in mapping
            }
            if len(candidates) == 1:
                mapping.update(candidates)
            else:
                valid_candidates = {
                    k: v
                    for k, v in candidates.items()
                    if all(
                        [
                            len(set(v) & set(y)) == len(set(digits[k]) & set(digits[x]))
                            for x, y in mapping.items()
                        ]
                    )
                }
                if len(valid_candidates) == 1:
                    mapping.update(valid_candidates)
        i = (i + 1) % 10
    return mapping


if __name__ == "__main__":
    main()
