import operator
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from math import prod

from tqdm import tqdm

from advent2022.utils.utils import Advent

advent = Advent(11)


def main():
    lines = advent.get_input_lines()
    monkeys = get_monkeys(lines)
    print(monkeys)
    cnt = Counter()
    for _ in range(20):
        play_round(monkeys, cnt, True)
    advent.submit(1, prod([x[1] for x in cnt.most_common(2)]))

    monkeys = get_monkeys(lines)
    cnt = Counter()
    for _ in tqdm(range(10000)):
        play_round(monkeys, cnt, False)
    advent.submit(2, prod([x[1] for x in cnt.most_common(2)]))


@dataclass
class Monkey:
    id: int = -1
    items: list[int] = field(default_factory=list)
    op: Callable[[int, int], int] = operator.add
    factor: int = -1
    mod: int = -1
    send_true: int = -1
    send_false: int = -1


def get_monkeys(lines: list[str]) -> dict[int, Monkey]:
    monkeys: dict[int, Monkey] = {}
    monkey = Monkey()
    for line in lines:
        if line.startswith("Monkey "):
            id = int(line[len("Monkey ") : -1])
            if id > 0:
                monkeys[id - 1] = monkey
                monkey = Monkey()
            monkey.id = id
        elif line.startswith("Starting items: "):
            monkey.items = [int(x) for x in line[len("Starting items: ") :].split(",")]
        elif line.startswith("Operation: new = "):
            if "+" in line[len("Operation: new = ") :]:
                monkey.op = operator.add
                monkey.factor = int(line[line.index("+") + 1 :])
            else:
                monkey.op = operator.mul
                try:
                    monkey.factor = int(line[line.index("*") + 1 :])
                except ValueError:
                    monkey.op = operator.pow
                    monkey.factor = 2
        elif line.startswith("Test: divisible by "):
            monkey.mod = int(line[len("Test: divisible by ") :])
        elif line.startswith("If true: throw to monkey "):
            monkey.send_true = int(line[len("If true: throw to monkey ") :])
        elif line.startswith("If false: throw to monkey "):
            monkey.send_false = int(line[len("If false: throw to monkey ") :])
    monkeys[id] = monkey
    return monkeys


def play_round(monkeys: dict[int, Monkey], cnt: Counter, part1: bool = True):
    supermod = prod([m.mod for m in monkeys.values()])
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        for item in monkey.items:
            new = monkey.op(item, monkey.factor)
            if part1:
                new = new // 3
            elif new > supermod:
                new = new % supermod
            if new % monkey.mod == 0:
                monkeys[monkey.send_true].items.append(new)
            else:
                monkeys[monkey.send_false].items.append(new)
            cnt[i] += 1
        monkey.items = []


if __name__ == "__main__":
    main()
