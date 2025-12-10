import heapq
from dataclasses import dataclass
from typing import TypeAlias

import z3
from z3 import Sum

from advent.utils import Advent

advent = Advent(10, 2025)

Lights: TypeAlias = tuple[bool, ...]
Button: TypeAlias = tuple[int, ...]
Joltages: TypeAlias = tuple[int, ...]


@dataclass
class Machine:
    lights: Lights
    buttons: list[Button]
    joltages: Joltages


def main():
    lines = advent.get_input_lines()
    machines = parse_input(lines)

    total = 0
    for machine in machines:
        presses, _ = dijkstra(machine.lights, machine.buttons)
        if presses is None:
            raise RuntimeError(f"Unable to solve machine {machine}.")
        total += presses
    advent.submit(1, total)

    total = 0
    for machine in machines:
        presses = solve_z3(machine.joltages, machine.buttons)
        if presses is None:
            raise RuntimeError(f"Unable to solve machine {machine}.")
        total += presses
    advent.submit(2, total)


def solve_z3(joltages: Joltages, buttons: list[Button]) -> int | None:
    s = z3.Optimize()
    P = [z3.Int(f"{idx}press") for idx in range(len(buttons))]
    for p in P:
        s.add(p >= 0)

    for j in range(len(joltages)):
        vars = [P[idx] for idx, button in enumerate(buttons) if j in button]
        s.add(Sum(vars) == joltages[j])

    s.minimize(Sum(P))

    if s.check() == z3.sat:
        m = s.model()
        return sum([m.eval(p).as_long() for p in P])

    return None


def dijkstra(lights: Lights, buttons: list[Button]) -> tuple[int | None, list[Button]]:
    visited = set()
    start = tuple([False for _ in range(len(lights))])
    distance = {start: 0}
    queue: list[tuple[int, Lights, list[Button]]] = [(0, start, [])]

    while queue:
        dist, node, path = heapq.heappop(queue)

        if node == lights:
            return dist, path

        if node not in visited:
            visited.add(node)

            for button in buttons:
                new_dist = dist + 1
                neighbor = press_light_button(node, button)
                if neighbor not in distance or new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor, path + [button]))

    return None, []


def press_light_button(lights: Lights, button: Button) -> Lights:
    new_lights = [light for light in lights]
    for idx in button:
        new_lights[idx] = not new_lights[idx]
    return tuple(new_lights)


def parse_input(lines: list[str]) -> list[Machine]:
    machines = []
    for line in lines:
        elements = line.split()
        lights = tuple(map(lambda x: x == "#", elements[0][1:-1]))
        joltages = tuple(map(int, elements[-1][1:-1].split(",")))
        buttons = [tuple(map(int, elt[1:-1].split(","))) for elt in elements[1:-1]]
        machines.append(Machine(lights, buttons, joltages))

    return machines


if __name__ == "__main__":
    main()
