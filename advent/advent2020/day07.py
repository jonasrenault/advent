import re

from advent.utils import Advent

advent = Advent(7, 2020)


def main():
    lines = advent.get_input_lines()
    rules = get_rules(lines)

    contains = {"shiny gold"}
    possible = set()
    while len(contains):
        contain = contains.pop()
        new_type = set([k for k, v in rules.items() if contain in [t for c, t in v]])
        contains.update(new_type)
        possible.update(new_type)
    advent.submit(1, len(possible))

    advent.submit(2, needs(rules, "shiny gold", "1") - 1)


def needs(rules, type: str, qty: str):
    if not rules[type]:
        return int(qty)

    return int(qty) + int(qty) * sum([needs(rules, t, c) for c, t in rules[type]])


def get_rules(lines):
    rules = {}
    for line in lines:
        key, types = line.split("bags contain")
        types = types.split(",")
        types = [get_type(t) for t in types if "no other bags" not in t]
        rules[key.strip()] = types
    return rules


def get_type(type):
    m = re.match(r"(\d+) ([a-z\s]+) bags?", type.strip())
    return m.groups()


if __name__ == "__main__":
    main()
