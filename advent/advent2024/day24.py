import operator
from collections.abc import Callable
from copy import copy
from typing import cast

from advent.utils.utils import Advent

advent = Advent(24, 2024)

GATE = tuple[str, Callable[[int, int], int], str, str]
OPS = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}


def main():
    lines = advent.get_input_lines()
    wires, values, gates = read_input(lines)

    advent.submit(1, run(wires, values, gates))

    wrong = check_parallel_adders(wires, gates)
    advent.submit(2, ",".join(sorted(wrong)))


def find_gate(op1: str | None, op2: str | None, op: str, gates: list[GATE]) -> str | None:
    for left, gate, right, out in gates:
        if gate is OPS[op] and left in (op1, op2) and right in (op1, op2):
            return out
    return None


def swap_output_wires(wire_a: str, wire_b: str, gates: list[GATE]):
    swaped = []
    for left, gate, right, out in gates:
        if out == wire_a:
            swaped.append((left, gate, right, wire_b))
        if out == wire_b:
            swaped.append((left, gate, right, wire_a))
        else:
            swaped.append((left, gate, right, out))
    return swaped


def check_parallel_adders(wires: set[str], gates: list[GATE]):
    zgates = sorted([wire for wire in wires if wire.startswith("z")])
    bits = int(zgates[-1][1:])
    current_carry_wire = None
    wrong = set()
    bit = 0

    while bit < bits:
        x_wire = f"x{bit:02d}"
        y_wire = f"y{bit:02d}"
        z_wire = f"z{bit:02d}"

        if bit == 0:
            current_carry_wire = find_gate(x_wire, y_wire, "AND", gates)
        else:
            ab_xor_gate = find_gate(x_wire, y_wire, "XOR", gates)
            ab_and_gate = find_gate(x_wire, y_wire, "AND", gates)
            cin_ab_xor_gate = find_gate(ab_xor_gate, current_carry_wire, "XOR", gates)
            if cin_ab_xor_gate is None:
                wrong.add(ab_xor_gate)
                wrong.add(ab_and_gate)
                gates = swap_output_wires(
                    cast(str, ab_xor_gate), cast(str, ab_xor_gate), gates
                )
                continue
            if cin_ab_xor_gate != z_wire:
                wrong.add(cin_ab_xor_gate)
                wrong.add(z_wire)
                gates = swap_output_wires(cin_ab_xor_gate, z_wire, gates)
                continue
            cin_ab_and_gate = find_gate(ab_xor_gate, current_carry_wire, "AND", gates)
            current_carry_wire = find_gate(ab_and_gate, cin_ab_and_gate, "OR", gates)
        bit += 1
    return wrong


def read_val(values: dict[str, int], var: str):
    out = ""
    for key in sorted(values.keys()):
        if key.startswith(var):
            out += str(values[key])
    return int(out[::-1], base=2)


def run(wires: set[str], values: dict[str, int], gates: list[GATE]) -> int:
    values = copy(values)
    while len(wires) > len(values.keys()):
        tick(values, gates)

    return read_val(values, "z")


def tick(values: dict[str, int], gates: list[GATE]):
    for left, gate, right, out in gates:
        if left in values and right in values:
            values[out] = gate(values[left], values[right])


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
            gates.append((left, OPS[gate], right, out))

    wires = set(values.keys())
    for left, _, right, out in gates:
        wires.update((left, right, out))
    return wires, values, gates


if __name__ == "__main__":
    main()
