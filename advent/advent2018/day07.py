import heapq
import re
from collections import defaultdict
from string import ascii_uppercase

from advent.utils import Advent

advent = Advent(7, 2018)


def main():
    lines = advent.get_input_lines()
    steps, conditions = read_graph(lines)
    done = solve_graph(steps, conditions)
    advent.submit(1, done)

    steps, conditions = read_graph(lines)
    time, _ = solve_workers(steps, conditions)
    advent.submit(2, time)


def solve_workers(
    steps: set[str], conditions: dict[str, set[str]], nb_workers: int = 5
) -> tuple[int, str]:
    done = ""
    time = 0
    workers: list[tuple[int, str]] = []
    todo = steps - conditions.keys()
    while todo or workers:
        if todo and len(workers) < nb_workers:
            step = min(todo)
            todo.remove(step)
            heapq.heappush(workers, (time + ascii_uppercase.index(step) + 61, step))
        else:
            time, step = heapq.heappop(workers)
            done += step
            todo |= update_conditions(conditions, step)

    return time, done


def solve_graph(steps: set[str], conditions: dict[str, set[str]]) -> str:
    done = ""
    todo = steps - conditions.keys()
    while todo:
        step = min(todo)
        todo.remove(step)
        done += step
        todo |= update_conditions(conditions, step)

    return done


def update_conditions(conditions: dict[str, set[str]], step: str) -> set[str]:
    todo = set()
    for key, value in conditions.items():
        value.discard(step)
        if len(value) == 0:
            todo.add(key)

    for key in todo:
        del conditions[key]

    return todo


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
