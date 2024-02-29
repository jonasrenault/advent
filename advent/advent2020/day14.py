from collections.abc import Iterator
from itertools import product

from advent.utils.utils import Advent

advent = Advent(14, 2020)


def main():
    lines = advent.get_input_lines()
    memory = decoder1(lines)
    advent.submit(1, sum(memory.values()))

    memory = decoder2(lines)
    advent.submit(2, sum(memory.values()))


def decoder2(lines: list[str]) -> dict[int, int]:
    """
    Apply mask to memory adresses.

    Args:
        lines (list[str]): the instructions

    Returns:
        dict[int, int]: the memory
    """
    mask = None
    memory = {}
    for line in lines:
        if line.startswith("mask"):
            mask = line[7:]
        elif mask is not None:
            mem = line[line.index("[") + 1 : line.index("]")]
            val = int(line[line.index("=") + 2 :])
            binm = str(bin(int(mem)))[2:]
            for mem in apply_mem_mask(mask, binm):
                memory[int(mem, 2)] = val
    return memory


def apply_mem_mask(mask: str, binm: str) -> Iterator[str]:
    """
    Mask a memory adress, yielding all possible memory adresses.

    Args:
        mask (str): the mask
        binm (str): the binary memory adress

    Yields:
        Iterator[str]: the floating memory adresses.
    """
    val = ""
    for i in range(1, len(mask) + 1):
        if mask[-i] == "X":
            val += "X"
        elif mask[-i] == "0":
            if i <= len(binm):
                val += binm[-i]
            else:
                val += "0"
        else:
            val += "1"
    val = val[::-1]
    yield from float_x(val)


def float_x(val: str) -> Iterator[str]:
    """
    Replace all X in bin val with possible combinations of 0 or 1.

    Args:
        val (str): a bin val with Xs

    Yields:
        Iterator[str]: bin val with 0 or 1 instead of X
    """
    nx = val.count("X")
    for pick in product("01", repeat=nx):
        nv = ""
        c = 0
        for v in val:
            if v == "X":
                nv += pick[c]
                c += 1
            else:
                nv += v
        yield nv


def decoder1(lines: list[str]) -> dict[str, int]:
    """
    Apply mask to values.

    Args:
        lines (list[str]): the instructions

    Returns:
        dict[str, int]: the memory
    """
    mask = None
    memory = {}
    for line in lines:
        if line.startswith("mask"):
            mask = line[7:]
        elif mask is not None:
            mem = line[line.index("[") + 1 : line.index("]")]
            val = int(line[line.index("=") + 2 :])
            binv = str(bin(val))[2:]
            val = int(apply_mask(mask, binv), 2)
            memory[mem] = val
    return memory


def apply_mask(mask: str, binv: str) -> str:
    """
    Mask a value.

    Args:
        mask (str): the mask
        binv (str): the binary value

    Returns:
        str: the masked binary value
    """
    val = ""
    for i in range(1, len(mask) + 1):
        if mask[-i] != "X":
            val += mask[-i]
        elif i > len(binv):
            val += "0"
        else:
            val += binv[-i]
    return val[::-1]


if __name__ == "__main__":
    main()
