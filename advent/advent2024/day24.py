from advent.utils.utils import Advent

advent = Advent(24, 2024)

GATE = tuple[str, str, str, str]


def main():
    lines = advent.get_input_lines()
    wires, values, gates = read_input(lines)

    advent.submit(1, run(wires, values, gates))


def run(wires: set[str], values: dict[str, int], gates: list[GATE]) -> int:
    while len(wires) > len(values.keys()):
        tick(values, gates)

    out = ""
    keys = sorted(values.keys())
    for key in keys[keys.index("z00") :]:
        out += str(values[key])
    return int(out[::-1], base=2)


def tick(values: dict[str, int], gates: list[GATE]):
    for left, gate, right, out in gates:
        if left in values and right in values:
            if gate == "AND":
                values[out] = values[left] & values[right]
            elif gate == "OR":
                values[out] = values[left] | values[right]
            else:
                values[out] = values[left] ^ values[right]


def read_input(lines: list[str]) -> tuple[set[str], dict[str, int], list[GATE]]:
    values = dict()
    gates = list()
    for line in lines:
        if ":" in line:
            gate, val = line.split(": ")
            values[gate] = int(val)
        elif "->" in line:
            left, out = line.split(" -> ")
            left, gate, right = left.split(" ")
            gates.append((left, gate, right, out))

    wires = set(values.keys())
    for left, gate, right, out in gates:
        wires.update((left, right, out))
    return wires, values, gates


if __name__ == "__main__":
    main()
