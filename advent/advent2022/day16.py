import functools
import re
from collections.abc import Iterable

import numpy as np
import numpy.typing as npt

from advent2022.utils.utils import Advent

advent = Advent(16)


def main():
    lines = advent.get_input_lines()
    flows, tunnels = get_flows_and_tunnels(lines)
    distances, names = compute_distances(tunnels)

    advent.submit(1, open_valves(flows, distances, names, "AA", 30))
    advent.submit(2, open_valves(flows, distances, names, "AA", 26, with_elephant=True))


def open_valves(
    flows: dict[str, int],
    distances: npt.NDArray[np.int_],
    names: list[str],
    start: str,
    time_left: int,
    with_elephant: bool = False,
) -> int:

    @functools.lru_cache(maxsize=None)
    def dfs(node: str, to_open: tuple[str, ...], time_left: int) -> int:
        nonlocal flows, distances, names
        values = [
            flows[r] * (time_left - distances[names.index(node), names.index(r)] - 1)
            + dfs(r, rr, time_left - distances[names.index(node), names.index(r)] - 1)
            for r, rr in choose_one(to_open)
            if distances[names.index(node), names.index(r)] < time_left
        ]
        return max(values) if values else 0

    def dfs2(node: str, to_open: tuple[str, ...], time_left: int) -> int:
        """ "
        This is the solution from [betaveros]
        (https://github.com/betaveros/advent-of-code-2022/blob/main/p16.noul).
        What it does is run dfs for one man during 26secs, then run again dfs
        for 26secs on remaining open valves. It does not work on sample data,
        because it only works if time runs out before one man could open all valves.
        """
        nonlocal flows, distances, names
        values = [
            flows[r] * (time_left - distances[names.index(node), names.index(r)] - 1)
            + dfs2(r, rr, time_left - distances[names.index(node), names.index(r)] - 1)
            for r, rr in choose_one(to_open)
            if distances[names.index(node), names.index(r)] < time_left
        ]
        return max(values) if values else dfs("AA", to_open, 26)

    to_open = tuple([k for k, v in flows.items() if v > 0])
    if with_elephant:
        return dfs2(start, to_open, time_left)
    return dfs(start, to_open, time_left)


def choose_one(options: tuple[str, ...]) -> Iterable[tuple[str, tuple[str, ...]]]:
    for i in range(len(options)):
        yield options[i], options[:i] + options[i + 1 :]


def get_flows_and_tunnels(
    lines: list[str],
) -> tuple[dict[str, int], dict[str, list[str]]]:
    flows = {}
    tunnels = {}
    for line in lines:
        m = re.match(
            r"Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)$",
            line,
        )
        if m:
            flows[m.group(1)] = int(m.group(2))
            tunnels[m.group(1)] = m.group(3).split(", ")
    return flows, tunnels


def compute_distances(
    tunnels: dict[str, list[str]]
) -> tuple[npt.NDArray[np.int_], list[str]]:
    names = list(tunnels.keys())
    d = np.full((len(names), len(names)), 100)
    for n, ts in tunnels.items():
        for t in ts:
            d[names.index(n), names.index(t)] = 1

    for k in range(len(names)):
        for i in range(len(names)):
            for j in range(len(names)):
                d[i, j] = min(d[i, j], d[i, k] + d[k, j])

    return d, names


if __name__ == "__main__":
    main()
