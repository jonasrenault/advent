from itertools import product

from advent.utils import Advent

advent = Advent(19, 2020)


def main():
    lines = advent.get_input_lines()
    rules, messages = parse(lines)

    c = 0
    for m in messages:
        if len(m) == matched(rules, "0", m):
            c += 1
    advent.submit(1, c)

    p42 = get_patterns(rules, "42")
    p31 = get_patterns(rules, "31")
    psize = len(p42[0])

    c = 0
    for m in messages:
        if match_loop(psize, p31, p42, m):
            c += 1
    advent.submit(2, c)


def match_loop(psize: int, p31: list[str], p42: list[str], message: str) -> bool:
    """
    rule 0: 8 11
    rule 8: 42 | 42 8
    rule 11: 42 31 | 42 11 31
    This means a message matching rule 0 must match a pattern from 42 at least 2 times,
    and finish by a pattern from 31 at least one times, with the added constraint that
    there are more patterns from 42 than from 31
    This function return True if the message matches this rule

    Args:
        psize (int): the size of the patterns
        p31 (list[str]): the patterns for rule 31
        p42 (list[str]): the patterns for rule 42
        message (str): the message

    Returns:
        bool: True if message matches rule 0
    """
    if len(message) % psize != 0:
        return False

    seen42 = 0
    seen31 = 0
    for i in range(0, len(message), psize):
        chunk = message[i : i + psize]
        if seen42 < 2:
            # start must be a 42 pattern
            if chunk not in p42:
                return False
            seen42 += 1
        elif seen31 == 0:
            # if we've not seen a pattern from 31 yet,
            # match a pattern from either rule
            if chunk in p42:
                seen42 += 1
            elif chunk in p31:
                seen31 += 1
            else:
                return False
        else:
            # once we've seen a 31 pattern, only match 31 patterns
            if chunk in p31:
                seen31 += 1
            else:
                return False

    return seen42 > 1 and seen42 > seen31 > 0


def get_patterns(rules: dict[str, list[list[str]]], rule: str) -> list[str]:
    """
    Return list of patterns matched by the given rule.

    Args:
        rules (dict[str, list[list[str]]]): the rules
        rule (str): the rule

    Returns:
        list[str]: the list of patterns that the rule matches
    """
    p = rules[rule]
    if len(p) == 1 and not p[0][0].isdigit():
        return p[0]

    res = []
    for part in p:
        if len(part) == 1:
            res.extend(get_patterns(rules, part[0]))
        else:
            p0, p1 = part
            left = get_patterns(rules, p0)
            right = get_patterns(rules, p1)
            res.extend([sub1 + sub2 for sub1, sub2 in product(left, right)])

    return res


def matched(rules: dict[str, list[list[str]]], rule: str, message: str) -> int:
    ors = rules[rule]
    if len(ors) == 1:
        ands = ors[0]
        if not ands[0].isdigit():
            # end case, check first char matches a or b
            if message[0] == ands[0]:
                return 1
            return -1
        else:
            return match_ands(rules, ands, message)
    else:
        for ands in ors:
            c = match_ands(rules, ands, message)
            if c > 0:
                return c
        return -1


def match_ands(rules: dict[str, list[list[str]]], ands: list[str], message: str) -> int:
    c = 0
    for r in ands:
        m = matched(rules, r, message[c:])
        if m < 0:
            return -1
        c += m
    return c


def parse(lines: list[str]) -> tuple[dict[str, list[list[str]]], list[str]]:
    rules = {}
    messages = []
    for line in lines:
        if not line:
            continue
        if line[0].isdigit():
            key = line[: line.index(":")]
            rule = line[line.index(":") + 1 :].replace('"', "")
            parts = rule.split("|")
            alts = [[x.strip() for x in r.strip().split(" ")] for r in parts]
            rules[key] = alts
        else:
            messages.append(line)

    return rules, messages


if __name__ == "__main__":
    main()
