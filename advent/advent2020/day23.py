from tqdm import tqdm

from advent.utils import Advent

advent = Advent(23, 2020)


def main():
    lines = advent.get_input_lines()
    cups = [int(c) for c in lines[0]]
    curr = cups[0]
    for _ in tqdm(range(100)):
        cups, curr = move(cups, curr)

    advent.submit(1, "".join(map(str, cups[cups.index(1) + 1 :] + cups[: cups.index(1)])))

    cups = [int(c) for c in lines[0]]
    clockwise = get_links(cups)
    curr = cups[0]
    for _ in tqdm(range(10000000)):
        move2(clockwise, curr, 1000000)
        curr = clockwise[curr]

    n1 = clockwise[1]
    n2 = clockwise[n1]
    advent.submit(2, n1 * n2)


def move2(clockwise: dict[int, int], current: int, highest: int):
    """
    Move cups in a dict of links.

    Args:
        clockwise (dict[int, int]): the dict of clockwise cups
        current (int): the current cup
        highest (int): the highest cup label
    """
    # get values of 3 picked up cups
    pick_up = []
    p = current
    for _ in range(3):
        p = clockwise.get(p, p + 1)
        pick_up.append(p)

    # get value of dest cup
    dest = current - 1
    while dest in pick_up or dest < 1:
        dest -= 1
        if dest < 1:
            dest = highest

    # update clockwise positions
    clockwise[current] = clockwise.get(pick_up[-1], pick_up[-1] + 1)
    end = clockwise.get(dest, dest + 1)
    clockwise[dest] = pick_up[0]
    clockwise[pick_up[-1]] = end


def get_links(cups: list[int]) -> dict[int, int]:
    """
    Get dict of next clockwise cup.

    Args:
        cups (list[int]): list of cups

    Returns:
        dict[int, int]: dict of clockwise cup
    """
    clockwise = dict()
    cmax = max(cups)
    for i in range(len(cups)):
        if i < len(cups) - 1:
            clockwise[cups[i]] = cups[i + 1]
        else:
            clockwise[cups[i]] = cmax + 1
    clockwise[1000000] = cups[0]
    return clockwise


def move(cups: list[int], current: int) -> tuple[list[int], int]:
    """
    Move cups in an array.

    Args:
        cups (list[int]): list of cups
        current (int): current cup

    Returns:
        tuple[list[int], int]: updated list of cups and new current cup
    """
    # pick up cups
    curr_idx = cups.index(current)
    pick_up_idx = [(curr_idx + i) % len(cups) for i in range(1, 4)]
    pick_up = [cups[i] for i in pick_up_idx]

    # remove picked_up cups
    for v in pick_up:
        cups.remove(v)

    # pick dest cup
    dest = current - 1
    while dest not in cups:
        dest -= 1
        if dest < min(cups):
            dest = max(cups)

    dest_idx = cups.index(dest)
    cups = cups[: dest_idx + 1] + pick_up + cups[dest_idx + 1 :]
    new_curr = cups[(cups.index(current) + 1) % len(cups)]
    return cups, new_curr


if __name__ == "__main__":
    main()
