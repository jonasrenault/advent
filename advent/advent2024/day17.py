from itertools import batched

import z3

from advent.utils import Advent

advent = Advent(17, 2024)


def main():
    lines = advent.get_input_lines()
    A, B, C, program = read_input(lines)

    A, B, C, output = run(A, B, C, program, 0)
    advent.submit(1, ",".join(list(map(str, output))))

    A0 = solve(program)
    advent.submit(2, A0)


def solve(program: tuple[int, ...]) -> int:
    b0idx = program.index(1)
    b1idx = program.index(1, b0idx + 2)
    b0 = program[b0idx + 1]
    b1 = program[b1idx + 1]
    s = z3.Optimize()
    orig = a = z3.BitVec("a", 64)

    for x in program:
        b = a & 7
        b ^= b0
        c = a >> b
        b ^= b1
        b ^= c
        a = a >> 3
        s.add((b & 7) == x)

    s.add(a == 0)
    s.minimize(orig)
    assert s.check() == z3.sat
    return s.model().eval(orig).as_long()


def bin_digits(bina: str):
    for v in batched(bina[::-1], n=3):
        yield int("".join(v).zfill(3), base=2)


def read_input(lines: list[str]) -> tuple[int, int, int, tuple[int, ...]]:
    A = int(lines[0][lines[0].index(":") + 1 :])
    B = int(lines[1][lines[1].index(":") + 1 :])
    C = int(lines[2][lines[2].index(":") + 1 :])
    program = tuple(map(int, lines[4][lines[4].index(":") + 1 :].split(",")))
    return A, B, C, program


def run(
    A: int, B: int, C: int, program: tuple[int, ...], pointer: int
) -> tuple[int, int, int, list[int]]:
    output = []
    while pointer < len(program):
        A, B, C, pointer, out = instruction(A, B, C, program, pointer)
        if out is not None:
            output.append(out)
    return A, B, C, output


def instruction(
    A: int, B: int, C: int, program: tuple[int, ...], pointer: int
) -> tuple[int, int, int, int, int | None]:
    opcode = program[pointer]
    operand = program[pointer + 1]

    if opcode == 0:  # adv
        return int(A / pow(2, combo(A, B, C, operand))), B, C, pointer + 2, None
    if opcode == 6:  # bdv
        return A, int(A / pow(2, combo(A, B, C, operand))), C, pointer + 2, None
    if opcode == 7:  # cdv
        return A, B, int(A / pow(2, combo(A, B, C, operand))), pointer + 2, None
    if opcode == 1:  # bxl
        return A, B ^ operand, C, pointer + 2, None
    if opcode == 2:  # bst
        return A, combo(A, B, C, operand) % 8, C, pointer + 2, None
    if opcode == 3 and A == 0:  # jnz
        return A, B, C, pointer + 2, None
    if opcode == 3 and A != 0:  # jnz
        return A, B, C, operand, None
    if opcode == 4:  # bxc
        return A, B ^ C, C, pointer + 2, None
    if opcode == 5:  # out
        return A, B, C, pointer + 2, combo(A, B, C, operand) % 8

    return A, B, C, pointer, None


def combo(A: int, B: int, C: int, operand: int) -> int:
    if operand < 4:
        return operand
    return [A, B, C][operand - 4]


if __name__ == "__main__":
    main()
