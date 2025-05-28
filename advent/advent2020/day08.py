from tqdm import tqdm

from advent.utils import Advent

advent = Advent(8, 2020)


def main():
    lines = advent.get_input_lines()
    advent.submit(1, run(lines)[0])
    advent.submit(2, run_all(lines))


def run_all(prog: list[str]) -> int:
    for idx, line in tqdm(enumerate(prog)):
        if line.startswith("nop"):
            acc, finished = run(prog[:idx] + ["jmp" + line[3:]] + prog[idx + 1 :])
            if finished:
                return acc
        elif line.startswith("jmp"):
            acc, finished = run(prog[:idx] + ["nop" + line[3:]] + prog[idx + 1 :])
            if finished:
                return acc
    return -1


def run(prog: list[str]) -> tuple[int, bool]:
    acc = 0
    idx = 0
    seen = set()
    while idx not in seen and idx < len(prog):
        seen.add(idx)
        op, val = parse_op(prog[idx])
        if op == "nop":
            idx += 1
        elif op == "acc":
            acc += val
            idx += 1
        elif op == "jmp":
            idx += val
    return acc, idx == len(prog)


def parse_op(line: str) -> tuple[str, int]:
    op, val = line.split()
    return op, int(val)


if __name__ == "__main__":
    main()
