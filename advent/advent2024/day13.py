import re
from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(13, 2024)


def main():
    lines = advent.get_input_lines()
    machines = read_input(lines)
    solutions = solve(machines)
    advent.submit(
        1, sum([min([3 * A + B for A, B in solution]) for solution in solutions.values()])
    )


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
