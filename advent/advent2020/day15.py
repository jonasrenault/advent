from tqdm import tqdm

from advent.utils import Advent

advent = Advent(15, 2020)


def main():
    lines = advent.get_input_lines()
    history = [int(x) for x in lines[0].split(",")]
    cache = {k: (i + 1,) for i, k in enumerate(history)}
    advent.submit(1, run(history[-1], cache, len(history), 2020))

    cache = {k: (i + 1,) for i, k in enumerate(history)}
    advent.submit(2, run(history[-1], cache, len(history), 30000000))


def run(last: int, cache: dict[int, tuple[int, ...]], turn: int, limit: int) -> int:
    for i in tqdm(range(turn + 1, limit + 1)):
        is_first = len(cache[last]) == 1
        if is_first:
            last = 0
        else:
            last = i - 1 - cache[last][1]

        if last in cache:
            cache[last] = (i, cache[last][0])
        else:
            cache[last] = (i,)
    return last


if __name__ == "__main__":
    main()
