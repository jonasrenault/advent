import re
from collections import defaultdict

import z3

from advent.utils.utils import Advent

advent = Advent(13, 2024)


def main():
    lines = advent.get_input_lines()
    machines = read_input(lines)
    solutions = solve(machines)
    advent.submit(
        1, sum([min([3 * A + B for A, B in solution]) for solution in solutions.values()])
    )

    total = 0
    for machine in machines:
        solution = solve_z3(*machine)
        if solution is not None:
            total += solution
    advent.submit(2, total)


def read_input(
    lines: list[str],
) -> list[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]]:
    machines = []
    for line in lines:
        if "A" in line:
            A = tuple(map(int, re.findall(r"[0-9]+", line)))
        elif "B" in line:
            B = tuple(map(int, re.findall(r"[0-9]+", line)))
        elif line:
            target = tuple(map(int, re.findall(r"[0-9]+", line)))
        else:
            machines.append((A, B, target))
    machines.append((A, B, target))
    return machines


def solve_z3(A, B, target, offset=10000000000000) -> int | None:
    xA, yA = A
    xB, yB = B
    xT, yT = target

    s = z3.Optimize()
    apress = z3.Int("apress")
    bpress = z3.Int("bpress")

    s.add(apress > 0)
    s.add(bpress > 0)
    s.add(xA * apress + xB * bpress == xT + offset)
    s.add(yA * apress + yB * bpress == yT + offset)
    s.minimize(apress * 3 + bpress)

    if s.check() == z3.sat:
        m = s.model()
        return m.eval(apress).as_long() * 3 + m.eval(bpress).as_long()

    return None


def solve(machines: list[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]]):
    solutions = defaultdict(list)
    for a in range(100):
        for b in range(100):
            for (xA, yA), (xB, yB), (xT, yT) in machines:
                if a * xA + b * xB == xT and a * yA + b * yB == yT:
                    solutions[(xA, yA), (xB, yB), (xT, yT)].append((a, b))
    return solutions


if __name__ == "__main__":
    main()
