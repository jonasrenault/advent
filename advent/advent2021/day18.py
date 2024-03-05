import json
import re
from itertools import product
from math import ceil, floor
from typing import Any

from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(18, 2021)


def main():
    lines = advent.get_input_lines()
    value = lines[0]
    for number in lines[1:]:
        value = add(value, number)
    advent.submit(1, magnitude(json.loads(value)))

    max_magnitude = 0
    for left, right in tqdm(product(lines, repeat=2)):
        magn = magnitude(json.loads(add(left, right)))
        if magn > max_magnitude:
            max_magnitude = magn
    advent.submit(2, max_magnitude)


def magnitude(value: list[Any] | int) -> int:
    if isinstance(value, int):
        return value

    left, right = value
    return 3 * magnitude(left) + 2 * magnitude(right)


def add(left: str, right: str) -> str:
    number = f"[{left},{right}]"
    reduced = reduce(number)
    while reduced != number:
        number = reduced
        reduced = reduce(number)
    return number


def add_to_regular(elements: list[str], value: str, left: bool = False) -> list[str]:
    updated = []
    added = False
    add_to = reversed(elements) if left else elements
    for elmt in add_to:
        if elmt not in ("[],") and not added:
            updated.append(str(int(elmt) + int(value)))
            added = True
        else:
            updated.append(elmt)
    if left:
        return updated[::-1]
    return updated


def reduce(number: str) -> str:
    listopen = 0
    expl_start_idx = 0
    expl_stop_idx = -1
    split_idx = -1

    # Loop through all the elements
    elements = [e for e in re.split(r"([,\]\[])", number) if e]
    for idx, elmt in enumerate(elements):
        if elmt == "[":
            listopen += 1
            expl_start_idx = idx
        elif elmt == "]":
            listopen -= 1
            if listopen >= 4:
                expl_stop_idx = idx
                break  # we found a list to explode, break
        elif elmt != ",":
            split_val = int(elmt)
            if split_val >= 10 and split_idx == -1:
                split_idx = idx

    # If we found a list to explode, explode it first
    if expl_stop_idx != -1:
        left = elements[expl_start_idx + 1]
        right = elements[expl_stop_idx - 1]
        return "".join(
            add_to_regular(elements[:expl_start_idx], left, True)
            + ["0"]
            + add_to_regular(elements[expl_stop_idx + 1 :], right)
        )

    # If we found a value to split, split it
    if split_idx != -1:
        split_val = int(elements[split_idx])
        return "".join(
            elements[:split_idx]
            + [f"[{floor(split_val / 2)},{ceil(split_val / 2)}]"]
            + elements[split_idx + 1 :]
        )

    # No operation, just return the input
    return "".join(elements)


if __name__ == "__main__":
    main()
