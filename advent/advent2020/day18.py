import re
from math import prod

from advent.utils import Advent

advent = Advent(18, 2020)


def main():
    lines = advent.get_input_lines()
    s = sum([solve(line) for line in lines])
    advent.submit(1, s)

    s2 = sum([solve2(line) for line in lines])
    advent.submit(2, s2)


def solve2(expr: str):
    # 1st find groups and solve them
    no_groups = ""
    previous = 0
    for s, e in get_groups(expr):
        no_groups += expr[previous:s] + str(solve2(expr[s + 1 : e]))
        previous = e + 1
    # no_groups expr now has no parentheses in it
    no_groups += expr[previous:]

    elmts = re.split(r"([\+\*])", no_groups)
    # first solve additions
    no_adds = []
    for i in range(1, len(elmts) - 1, 2):
        if elmts[i] == "+":
            val = int(elmts[i - 1]) + int(elmts[i + 1])
            elmts[i + 1] = val
        elif elmts[i] == "*":
            no_adds.append(int(elmts[i - 1]))
    # no_adds is a list of ints
    no_adds.append(int(elmts[-1]))

    # finally solve multiplications
    return prod(no_adds)


def solve(expr: str) -> int:
    # 1st find groups and solve them
    no_groups = ""
    previous = 0
    for s, e in get_groups(expr):
        no_groups += expr[previous:s] + str(solve(expr[s + 1 : e]))
        previous = e + 1
    # no_groups expr now has no parentheses in it
    no_groups += expr[previous:]

    # solve expr from left to right
    elmts = re.split(r"([\+\*])", no_groups)
    val = int(elmts[0])
    for i in range(1, len(elmts) - 1, 2):
        if elmts[i] == "+":
            val += int(elmts[i + 1])
        else:
            val *= int(elmts[i + 1])
    return val


def get_groups(expr: str) -> list[tuple[int, int]]:
    """
    Return the indices of the outermost parenthese groups in expr.

    Args:
        expr (str): the expression

    Returns:
        list[tuple[int, int]]: the list of indices
    """
    groups = []
    start = -1
    o = 0
    c = 0
    for i, e in enumerate(expr):
        if e == "(":
            if o == 0:
                start = i
            o += 1
        if e == ")":
            c += 1
            if c == o:
                groups.append((start, i))
                o = 0
                c = 0
    return groups


if __name__ == "__main__":
    main()
