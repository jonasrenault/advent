from advent.utils.utils import Advent

advent = Advent(8, 2018)


def main():
    lines = advent.get_input_lines()
    numbers = list(map(int, lines[0].split()))
    advent.submit(1, sum(read_metadatas(numbers)))

    numbers = list(map(int, lines[0].split()))
    advent.submit(2, read_values(numbers))


def read_metadatas(numbers: list[int]) -> list[int]:
    children = numbers.pop(0)
    metadatas = numbers.pop(0)
    metadata = []
    for _ in range(children):
        metadata.extend(read_metadatas(numbers))
    metadata.extend([numbers.pop(0) for _ in range(metadatas)])
    return metadata


def read_values(numbers: list[int]) -> int:
    children = numbers.pop(0)
    metadatas = numbers.pop(0)
    children_values = [read_values(numbers) for _ in range(children)]
    metadata = [numbers.pop(0) for _ in range(metadatas)]

    if children == 0:
        return sum(metadata)
    value = 0
    for idx in metadata:
        try:
            value += children_values[idx - 1]
        except IndexError:
            pass
    return value


if __name__ == "__main__":
    main()
