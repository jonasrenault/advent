from advent.utils import Advent

advent = Advent(2, 2020)


def main():
    lines = advent.get_input_lines()
    pwds = parse_pwds(lines)
    valid_pwds = [pwd for pwd in pwds if is_valid(*pwd)]
    advent.submit(1, len(valid_pwds))

    valid_pwds2 = [pwd for pwd in pwds if is_valid_2(*pwd)]
    advent.submit(2, len(valid_pwds2))


def is_valid(pwd: str, key: str, counts: list[int]) -> bool:
    count = pwd.count(key)
    return min(counts) <= count <= max(counts)


def is_valid_2(pwd: str, key: str, counts: list[int]) -> bool:
    ok = [pwd[c - 1] == key for c in counts]
    return any(ok) and not all(ok)


def parse_pwds(lines: list[str]) -> list[tuple[str, str, list[int]]]:
    pwds = []
    for line in lines:
        idx = line.index(":")
        pwd = line[idx + 2 :].strip()
        key = line[idx - 1]
        counts = [int(x.strip()) for x in line[: idx - 1].split("-")]
        pwds.append((pwd, key, counts))
    return pwds


if __name__ == "__main__":
    main()
