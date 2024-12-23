from itertools import combinations

from advent.utils.utils import Advent

advent = Advent(23, 2024)


def main():
    lines = advent.get_input_lines()
    computers, connections = get_connections(lines)
    triplets = get_groups(computers, connections)
    triplets_with_t = [
        triplet for triplet in triplets if any([node.startswith("t") for node in triplet])
    ]
    advent.submit(1, len(triplets_with_t))


def get_groups(
    computers: set[str], connections: set[str], size: int = 3
) -> set[tuple[str, ...]]:
    triplets = set()
    for nodes in combinations(computers, size):
        for left, right in combinations(nodes, 2):
            if "".join(sorted([left, right])) not in connections:
                break
        else:
            triplets.add(nodes)
    return triplets


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
