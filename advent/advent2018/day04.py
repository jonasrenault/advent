import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from operator import itemgetter

from advent.utils import Advent

advent = Advent(4, 2018)


def main():
    lines = advent.get_input_lines()
    logs = get_logs(lines)
    logs.sort(key=itemgetter(0))

    counts = get_sleep_counts(logs)
    advent.submit(1, strategy_1(counts))
    advent.submit(2, strategy_2(counts))


def strategy_2(counts: dict[int, Counter]) -> int:
    best = 0
    guard_id = 0
    most_common = 0
    for id, sleeps in counts.items():
        total = sleeps.most_common(1)[0][1]
        if total > best:
            best = total
            most_common = sleeps.most_common(1)[0][0]
            guard_id = id
    return guard_id * most_common


def strategy_1(counts: dict[int, Counter]) -> int:
    best = 0
    guard_id = 0
    most_common = 0
    for id, sleeps in counts.items():
        total = sleeps.total()
        if total > best:
            best = total
            most_common = sleeps.most_common(1)[0][0]
            guard_id = id
    return guard_id * most_common


def get_sleep_counts(logs: list[tuple[datetime, str]]) -> dict[int, Counter]:
    guard = 0
    start = datetime.now()
    sleeps: defaultdict[int, Counter] = defaultdict(Counter)
    for date, log in logs:
        if log.startswith("Guard"):
            guard = int(re.findall(r"-?\d+", log)[0])
        elif log.startswith("falls"):
            start = date
        else:
            delta = date - start
            for td in (
                start + timedelta(minutes=m)
                for m in range(int(delta.total_seconds() // 60))
            ):
                sleeps[guard][td.minute] += 1
    return sleeps


def get_logs(lines: list[str]) -> list[tuple[datetime, str]]:
    logs = []
    for line in lines:
        datetime_str = line[6 : line.index("]")]
        date = datetime.strptime(datetime_str, "%m-%d %H:%M")
        logs.append((date, line[line.index("]") + 2 :]))
    return logs


if __name__ == "__main__":
    main()
