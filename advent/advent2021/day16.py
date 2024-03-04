from collections.abc import Callable
from math import prod

from advent.utils.utils import Advent

advent = Advent(16, 2021)


def main():
    lines = advent.get_input_lines()
    bits_input = hex_to_bits(lines[0])
    versions, _, _, _ = parse_packet(bits_input)
    advent.submit(1, sum(versions))

    _, _, values, _ = parse_packet_2(bits_input)
    advent.submit(2, values[0])


def parse_packet_2(bits_input: str) -> tuple[list[int], int, list[int], str]:
    version = int(bits_input[:3], 2)
    type_ = int(bits_input[3:6], 2)
    if type_ == 4:
        value, to_parse = parse_literal_value(bits_input[6:])
        return [version], type_, [value], to_parse
    else:
        versions, values, to_parse = parse_operator(bits_input[6:], parse_packet_2)
        if type_ == 0:
            value = sum(values)
        elif type_ == 1:
            value = prod(values)
        elif type_ == 2:
            value = min(values)
        elif type_ == 3:
            value = max(values)
        elif type_ == 5:
            value = int(values[0] > values[1])
        elif type_ == 6:
            value = int(values[0] < values[1])
        elif type_ == 7:
            value = int(values[0] == values[1])
        return [version] + versions, type_, [value], to_parse


def parse_packet(bits_input: str) -> tuple[list[int], int, list[int], str]:
    version = int(bits_input[:3], 2)
    type_ = int(bits_input[3:6], 2)
    if type_ == 4:
        lvalue, to_parse = parse_literal_value(bits_input[6:])
        return [version], type_, [lvalue], to_parse
    else:
        versions, value, to_parse = parse_operator(bits_input[6:], parse_packet)
        return [version] + versions, type_, value, to_parse


def parse_literal_value(bits_input: str) -> tuple[int, str]:
    i = 0
    value = ""
    while bits_input[i] == "1":
        value += bits_input[i + 1 : i + 1 + 4]
        i += 5
    value += bits_input[i + 1 : i + 1 + 4]
    return int(value, 2), bits_input[i + 1 + 4 :]


def parse_operator(
    bits_input: str,
    parse_packet_func: Callable[[str], tuple[list[int], int, list[int], str]],
) -> tuple[list[int], list[int], str]:
    type_id = bits_input[0]
    if type_id == "0":
        return parse_operator_type_0(bits_input[1:], parse_packet_func)
    else:
        return parse_operator_type_1(bits_input[1:], parse_packet_func)


def parse_operator_type_0(
    bits_input: str,
    parse_packet_func: Callable[[str], tuple[list[int], int, list[int], str]],
) -> tuple[list[int], list[int], str]:
    total_length = int(bits_input[:15], 2)
    to_parse = bits_input[15:]
    current_length = len(to_parse)
    values = []
    versions = []
    while current_length - len(to_parse) < total_length:
        subversions, _, subvalues, to_parse = parse_packet_func(to_parse)
        versions.extend(subversions)
        values.extend(subvalues)
    return versions, values, to_parse


def parse_operator_type_1(
    bits_input, parse_packet_func
) -> tuple[list[int], list[int], str]:
    num_of_subpackets = int(bits_input[:11], 2)
    to_parse = bits_input[11:]
    values = []
    versions = []
    for _ in range(num_of_subpackets):
        subversions, _, subvalues, to_parse = parse_packet_func(to_parse)
        versions.extend(subversions)
        values.extend(subvalues)
    return versions, values, to_parse


def hex_to_bits(hex_input: str) -> str:
    num_of_bits = 4 * len(hex_input)
    return bin(int(hex_input, 16))[2:].zfill(num_of_bits)


if __name__ == "__main__":
    main()
