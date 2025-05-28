from math import lcm

from advent.utils import Advent

advent = Advent(13, 2020)


def main():
    lines = advent.get_input_lines()
    ts = int(lines[0])
    buses = [int(x.strip()) for x in lines[1].split(",") if x.strip() != "x"]
    earliest = [ts // b * b + b for b in buses]
    t = min(earliest)
    bus = buses[earliest.index(t)]
    wait = t - ts
    advent.submit(1, wait * bus)

    buses = [
        int(x.strip()) if x.strip() != "x" else x.strip() for x in lines[1].split(",")
    ]
    buses = [(b, i) for i, b in enumerate(buses) if b != "x"]
    step, time = buses[0]
    for b, d in buses[1:]:
        while (time + d) % b != 0:
            time += step
        step = lcm(step, b)
    advent.submit(2, time)


if __name__ == "__main__":
    main()
