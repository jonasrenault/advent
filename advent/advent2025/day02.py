from advent.utils import Advent

advent = Advent(2, 2025)


def main():
    lines = advent.get_input_lines()
    ranges = lines[0].split(",")

    invalids = []
    for range in ranges:
        invalids.extend(invalid_ids(*range.split("-")))
    advent.submit(1, sum(map(int, invalids)))

    invalids = []
    for range in ranges:
        invalids.extend(invalid_ids_2(*range.split("-")))
    advent.submit(2, sum(map(int, invalids)))


def invalid_ids(left: str, right: str) -> list[str]:
    start, end = left, right
    if len(start) % 2:
        start = "1" + ("0" * len(start))
    if len(end) % 2:
        end = "1" + ("0") * len(end)

    invalids = []
    for x in range(int(start[: len(start) // 2]), int(end[: len(end) // 2]) + 1):
        invalids.append(str(x) + str(x))

    invalids = [x for x in invalids if int(left) <= int(x) <= int(right)]
    return invalids


def invalid_ids_2(left: str, right: str) -> set[str]:
    if len(left) != len(right):
        return invalid_ids_2(left, "9" * len(left)) | invalid_ids_2(
            "1" + "0" * len(left), right
        )

    size = len(left)
    invalids = []
    for div in range(1, size):
        if size % div == 0:
            invalids.extend(
                [
                    size // div * str(x)
                    for x in range(int(left[:div]), int(right[:div]) + 1)
                ]
            )
    return set([x for x in invalids if int(left) <= int(x) <= int(right)])


if __name__ == "__main__":
    main()
