import numpy as np

from advent.utils.utils import Advent

advent = Advent(2, 2024)


def main():
    lines = advent.get_input_lines()
    reports = [tuple(map(int, line.split())) for line in lines]

    advent.submit(1, sum([is_safe(report) for report in reports]))
    advent.submit(2, sum([is_safe_tolerate(report) for report in reports]))


def is_safe_tolerate(report: tuple[int, ...]):
    return is_safe(report) or any(
        [is_safe(report[:idx] + report[idx + 1 :]) for idx in range(len(report))]
    )


def is_safe(report: tuple[int, ...]) -> bool:
    return all(
        [
            1 <= abs(report[idx] - report[idx + 1]) <= 3
            and np.sign(report[idx] - report[idx + 1]) == np.sign(report[0] - report[1])
            for idx in range(0, len(report) - 1)
        ]
    )


if __name__ == "__main__":
    main()
