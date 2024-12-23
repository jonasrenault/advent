from collections.abc import Iterable
from itertools import combinations

from advent.utils.utils import Advent

advent = Advent(23, 2024)


def main():
    lines = advent.get_input_lines()
    computers, connections = get_connections(lines)
    triplets = get_groups(computers, connections)
    triplets_with_t = [
        triplet
        for triplet in triplets
        if any([node.startswith("t") for node in triplet.split(",")])
    ]
    advent.submit(1, len(triplets_with_t))

    groups = triplets
    size = 3
    while len(groups) > 1:
        groups = find_bigger_group(computers, connections, groups)
        size += 1
        print(f"{len(groups)} {size}-plets.")

    advent.submit(2, groups.pop())


def find_bigger_group(computers: set[str], connections: set[str], groups: set[str]):
    bigger_group = set()
    for group in groups:
        for comp in computers:
            if comp not in group and is_connected_to_all(
                comp, group.split(","), connections
            ):
                g = ",".join(sorted(group.split(",") + [comp]))
                bigger_group.add(g)

    return bigger_group


def get_groups(computers: set[str], connections: set[str], size: int = 3) -> set[str]:
    groups = set()
    for nodes in combinations(computers, size):
        if is_all_connected(nodes, connections):
            groups.add(",".join(sorted(nodes)))
    return groups


def is_connected_to_all(node: str, nodes: Iterable[str], connections: set[str]) -> bool:
    for other_node in nodes:
        if "".join(sorted([node, other_node])) not in connections:
            return False
    return True


def is_all_connected(nodes: Iterable[str], connections: set[str]) -> bool:
    for left, right in combinations(nodes, 2):
        if "".join(sorted([left, right])) not in connections:
            return False
    return True


def get_connections(lines: list[str]) -> tuple[set[str], set[str]]:
    connections: set[str] = set()
    computers: set[str] = set()
    for connection in lines:
        left, right = connection.split("-")
        computers.add(left)
        computers.add(right)
        connections.add("".join(sorted([left, right])))
    return computers, connections


if __name__ == "__main__":
    main()
