from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(25, 2023)


def main():
    lines = advent.get_input_lines()
    connections = get_connections(lines)

    g1, g2 = split(connections)
    advent.submit(1, len(g1) * len(g2))


def split(connections: dict[str, set[str]]) -> tuple[set[str], set[str]]:
    """
    Split graph into two groups. Start with all components in same group, and remove
    components one by one until there are only 3 connections between the two groups.
    Remove components with the maximum number of connexions in the other group.

    See https://www.reddit.com/r/adventofcode/comments/18qbsxs/comment/ketzp94/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

    Args:
        connections (dict[str, set[str]]): the connexions graph

    Returns:
        tuple[set[str], set[str]]: two groups of components with at most 3
        connexions between them
    """
    g1 = set(connections)

    count = lambda v: len(connections[v] - g1)  # noqa: E731
    while sum(map(count, g1)) != 3:
        g1.remove(max(g1, key=count))

    return g1, set(connections) - g1


def get_connections(lines: list[str]) -> dict[str, set[str]]:
    """
    Get connections graph.

    Args:
        lines (list[str]): the input lines

    Returns:
        dict[str, set[str]]: the connexion graph
    """
    connections = defaultdict(set)
    for line in lines:
        left, right = line.split(": ")
        for other in right.split():
            connections[left].add(other)
            connections[other].add(left)
    return connections


if __name__ == "__main__":
    main()
