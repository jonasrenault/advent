import json
from itertools import batched
from typing import Any

from advent2022.utils.utils import Advent

advent = Advent(13)


def main():
    lines = advent.get_input_lines()
    pairs = get_pairs(lines)
    valid = [
        i + 1 for i, (left, right) in enumerate(pairs) if validate_pairs(left, right)
    ]
    advent.submit(1, sum(valid))

    packets = [packet for pair in pairs for packet in pair] + [[[2]], [[6]]]
    sorted = bubble_sort(packets)
    advent.submit(2, (sorted.index([[6]]) + 1) * (sorted.index([[2]]) + 1))


def bubble_sort(packets: list[list[Any]]) -> list[list[Any]]:
    sorted = True
    while sorted:
        sorted = False
        for i in range(len(packets) - 1):
            left = packets[i]
            right = packets[i + 1]
            if not validate_pairs(left, right):
                packets[i + 1] = left
                packets[i] = right
                sorted = True

    return packets


def validate_pairs(left: list[Any] | int, right: list[Any] | int) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    elif isinstance(left, list) and isinstance(right, list):
        for lv, rv in zip(left, right):
            res = validate_pairs(lv, rv)
            if res is None:
                continue
            else:
                return res
        if len(left) == len(right):
            return None
        return len(left) < len(right)
    elif isinstance(left, int):
        return validate_pairs([left], right)
    else:
        return validate_pairs(left, [right])


def get_pairs(lines: list[str]) -> list[tuple[Any, Any]]:
    pairs = []
    for left, right, _ in batched(lines + [""], 3):
        pairs.append((json.loads(left), json.loads(right)))
    return pairs


if __name__ == "__main__":
    main()
