from math import prod

from advent.utils.utils import Advent

advent = Advent(1, 2020)


def main():
    lines = advent.get_input_lines()
    lines = [int(x) for x in lines]
    pair = None
    for idx, x in enumerate(lines):
        for y in lines[idx + 1 :]:
            if x + y == 2020:
                pair = (x, y)
                break
        if pair:
            break
    advent.submit(1, prod(pair))

    triplet = None
    for idx, x in enumerate(lines):
        for idy, y in enumerate(lines[idx + 1 :]):
            for z in lines[idy + 1 :]:
                if x + y + z == 2020:
                    triplet = (x, y, z)
                    break
            if triplet:
                break
        if triplet:
            break
    advent.submit(2, prod(triplet))


if __name__ == "__main__":
    main()
