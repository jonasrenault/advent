from functools import lru_cache

from advent.utils import Advent

advent = Advent(11, 2025)


def main():
    lines = advent.get_input_lines()
    nodes = read_input(lines)

    advent.submit(1, count_paths("you", nodes))
    advent.submit(2, solve(nodes))


def solve(nodes: dict[str, tuple[str, ...]]) -> int:

    @lru_cache(maxsize=None)
    def count(node: str, fft: bool = False, dac: bool = False):
        nonlocal nodes
        if node == "out":
            return 1 if fft and dac else 0

        return sum(
            [
                count(output, fft or output == "fft", dac or output == "dac")
                for output in nodes[node]
            ]
        )

    return count("svr", False, False)


def count_paths(node: str, nodes: dict[str, tuple[str, ...]]) -> int:
    if node == "out":
        return 1

    return sum([count_paths(output, nodes) for output in nodes[node]])


def read_input(lines: list[str]) -> dict[str, tuple[str, ...]]:
    nodes: dict[str, tuple[str, ...]] = dict()
    for line in lines:
        head = line[:3]
        tail = tuple(line[5:].split())
        nodes[head] = tail
    return nodes


if __name__ == "__main__":
    main()
