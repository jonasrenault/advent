import operator
import re
from collections.abc import Callable
from dataclasses import dataclass

from advent2022.utils.utils import Advent

advent = Advent(21)

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

inv_ops = {
    operator.sub: operator.add,
    operator.add: operator.sub,
    operator.truediv: operator.mul,
    operator.mul: operator.truediv,
}


@dataclass
class Monkey:
    name: str
    value: int | None = None
    op: Callable[[int, int], int] | None = None
    left: str | None = None
    right: str | None = None


def main():
    lines = advent.get_input_lines()
    monkeys = get_monkeys(lines)
    advent.submit(1, solve_for_monkey(monkeys, "root"))
    advent.submit(2, int(solve_for_human(monkeys)))


def solve_for_human(monkeys: dict[str, Monkey]) -> float:
    monkeys["humn"] = Monkey("x")
    monkey = monkeys["root"]
    if monkey.left is not None and monkey.right is not None:
        try:
            value = solve_for_monkey(monkeys, monkey.right)
        except ValueError:
            tosolve = monkey.right
            value = solve_for_monkey(monkeys, monkey.left)
        else:
            tosolve = monkey.left
        return solve_for_x(monkeys, tosolve, value)
    return 0


def solve_for_x(monkeys: dict[str, Monkey], name: str, value: int) -> float:
    if name == "humn":
        return value
    monkey = monkeys[name]
    if monkey.op is not None and monkey.left is not None and monkey.right is not None:
        try:
            rval = solve_for_monkey(monkeys, monkey.right)
        except ValueError:
            if monkey.op == operator.sub:
                value = -value
            lval = solve_for_monkey(monkeys, monkey.left)
            return solve_for_x(monkeys, monkey.right, inv_ops[monkey.op](value, lval))
        else:
            return solve_for_x(monkeys, monkey.left, inv_ops[monkey.op](value, rval))
    return 0


def solve_for_monkey(monkeys: dict[str, Monkey], name: str) -> int:
    monkey = monkeys[name]
    if monkey.value is not None:
        return monkey.value
    if monkey.op is not None and monkey.left is not None and monkey.right is not None:
        return int(
            monkey.op(
                solve_for_monkey(monkeys, monkey.left),
                solve_for_monkey(monkeys, monkey.right),
            )
        )
    raise ValueError("Unknown Monkey")


def get_monkeys(lines: list[str]) -> dict[str, Monkey]:
    monkeys = {}
    for line in lines:
        m = re.match(r"(.+): (\d+)", line)
        if m:
            monkeys[m.group(1)] = Monkey(m.group(1), value=int(m.group(2)))
        else:
            m = re.match(r"(.+): ([^\+\/\-\*]+) ([\+\/\-\*]) ([^\+\/\-\*]+)", line)
            if m is not None:
                monkeys[m.group(1)] = Monkey(
                    m.group(1), left=m.group(2), right=m.group(4), op=ops[m.group(3)]
                )
    return monkeys


if __name__ == "__main__":
    main()
