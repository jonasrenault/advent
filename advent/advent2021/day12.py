from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(12, 2021)


def main():
    lines = advent.get_input_lines()
    graph = get_graph(lines)
    paths = get_paths(graph)
    advent.submit(1, len(paths))

    paths2 = get_paths(graph, double_small=True)
    advent.submit(2, len(paths2))


def get_graph(lines: list[str]) -> dict[str, set[str]]:
    graph = defaultdict(set)
    for line in lines:
        left, right = line.split("-")
        graph[left].add(right)
        graph[right].add(left)
    return graph


def get_paths(graph: dict[str, set[str]], double_small: bool = False) -> list[list[str]]:
    queue = [("start", ["start"], "")]
    paths = []

    while queue:
        node, visited, double_small_visited = queue.pop()
        if node == "end":
            paths.append(visited + ["end"])

        for n in graph[node]:
            if n.isupper() or n not in visited:
                queue.append((n, visited + [n], double_small_visited))
            elif (
                double_small and not double_small_visited and n != "start" and n != "end"
            ):
                queue.append((n, visited, n))

    return paths


if __name__ == "__main__":
    main()
