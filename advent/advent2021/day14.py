from collections import defaultdict

from advent.utils.utils import Advent

advent = Advent(14, 2021)


def main():
    lines = advent.get_input_lines()
    template = lines[0]
    pairs = dict()
    for line in lines[2:]:
        key, value = line.split(" -> ")
        pairs[key] = value

    polymer = lines[0]
    template = defaultdict(int)
    for i in range(len(polymer)):
        template[polymer[i]] += 1
        if i < len(polymer) - 1:
            template[polymer[i : i + 2]] += 1

    for _ in range(10):
        template = polymerize(template, pairs)
    counts = [value for key, value in template.items() if len(key) == 1]
    advent.submit(1, max(counts) - min(counts))

    for _ in range(30):
        template = polymerize(template, pairs)
    counts = [value for key, value in template.items() if len(key) == 1]
    advent.submit(2, max(counts) - min(counts))


def polymerize(template: dict[str, int], pairs: dict[str, str]) -> dict[str, int]:
    new_template: defaultdict[str, int] = defaultdict(int)
    for key, value in template.items():
        if key in pairs:
            new_template[key[0] + pairs[key]] += value
            new_template[pairs[key] + key[1]] += value
            new_template[pairs[key]] += value
        else:  # single letter, copy value
            new_template[key] += value
    return new_template


if __name__ == "__main__":
    main()
