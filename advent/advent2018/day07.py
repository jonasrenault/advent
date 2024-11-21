import re
from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(7, 2018)


def main():
    lines = advent.get_input_lines()
    steps, conditions = read_graph(lines)
    done = solve_graph(steps, conditions)
    advent.submit(1, done)


def solve_graph(steps: set[str], conditions: dict[str, set[str]]) -> str:
    done = ""
    todo = steps - conditions.keys()
    while todo:
        step = min(todo)
        todo.remove(step)
        done += step
        for key, value in conditions.items():
            value.discard(step)
            if len(value) == 0:
                todo.add(key)

        conditions = {key: value for key, value in conditions.items() if len(value) > 0}

    return done


def read_graph(lines: list[str]) -> tuple[set[str], dict[str, set[str]]]:
    conditions = defaultdict(set)
    steps = set()
    for line in lines:
        condition, step = re.findall(r"([A-Z])", line[1:])
        conditions[step].add(condition)
        steps.add(condition)
        steps.add(step)

    return steps, conditions


if __name__ == "__main__":
    main()
