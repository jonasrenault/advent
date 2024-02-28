import re
from collections import deque
from math import prod

from advent2022.utils.utils import Advent

advent = Advent(19)


def main():
    lines = advent.get_input_lines()
    blueprints = get_blueprints(lines)
    total = sum(bid * search(b) for bid, *b in blueprints)
    advent.submit(1, total)

    total = prod(search(b, 32) for _, *b in blueprints[:3])
    advent.submit(2, total)


def best_case_scenario(initial_amount: int, robots: int, t: int) -> int:
    return initial_amount + robots * (t + 1) + t * (t + 1) // 2


def search(blueprint: tuple[int, ...], time=24) -> int:
    rore_cost, rclay_cost, robs_cost_ore, robs_cost_clay, rgeo_cost_ore, rgeo_cost_obs = (
        blueprint
    )
    max_ore_needed = max(rore_cost, rclay_cost, robs_cost_ore, rgeo_cost_ore)
    max_clay_needed = robs_cost_clay
    max_obs_needed = rgeo_cost_obs

    best = 0
    visited = set()
    q = deque([(time, 0, 0, 0, 0, 1, 0, 0, 0)])

    while q:
        time, ore, clay, obs, geo, rore, rclay, robs, rgeo = state = q.pop()
        if state in visited:
            continue

        visited.add(state)

        # Each robot we have mines 1 resource of its type, taking 1 minute.
        newore = ore + rore
        newclay = clay + rclay
        newobs = obs + robs
        newgeo = geo + rgeo
        time -= 1

        # If we run out of time, we reached a "goal" state. Update the best
        # number of geodes we were able to mine.
        if time == 0:
            best = max(best, newgeo)
            continue

        if best_case_scenario(newgeo, rgeo, time) < best:
            continue

        if (
            best_case_scenario(newobs, robs, time) < rgeo_cost_obs
            or best_case_scenario(newore, rore, time) < rgeo_cost_ore
        ):
            best = max(best, newgeo + rgeo * time)
            continue

        if obs >= rgeo_cost_obs and ore >= rgeo_cost_ore:
            q.append(
                (
                    time,
                    newore - rgeo_cost_ore,
                    newclay,
                    newobs - rgeo_cost_obs,
                    newgeo,
                    rore,
                    rclay,
                    robs,
                    rgeo + 1,
                )
            )

        if robs < max_obs_needed and clay >= robs_cost_clay and ore >= robs_cost_ore:
            q.append(
                (
                    time,
                    newore - robs_cost_ore,
                    newclay - robs_cost_clay,
                    newobs,
                    newgeo,
                    rore,
                    rclay,
                    robs + 1,
                    rgeo,
                )
            )

        if rclay < max_clay_needed and ore >= rclay_cost:
            q.append(
                (
                    time,
                    newore - rclay_cost,
                    newclay,
                    newobs,
                    newgeo,
                    rore,
                    rclay + 1,
                    robs,
                    rgeo,
                )
            )

        if rore < max_ore_needed and ore >= rore_cost:
            q.append(
                (
                    time,
                    newore - rore_cost,
                    newclay,
                    newobs,
                    newgeo,
                    rore + 1,
                    rclay,
                    robs,
                    rgeo,
                )
            )

        if (
            (robs and obs < max_obs_needed)
            or (rclay and clay < max_clay_needed)
            or ore < max_ore_needed
        ):
            q.append(
                (
                    time,
                    newore,
                    newclay,
                    newobs,
                    newgeo,
                    rore,
                    rclay,
                    robs,
                    rgeo,
                )
            )

    return best


def get_blueprints(lines: list[str]) -> list[tuple[int, ...]]:
    exp = re.compile(r"\d+")
    blueprints = []

    for line in lines:
        blueprints.append(tuple(map(int, exp.findall(line))))

    return blueprints


if __name__ == "__main__":
    main()
