from advent.utils.utils import Advent

advent = Advent(9, 2024)


def main():
    lines = advent.get_input_lines()
    disk_map = get_disk_map(lines[0])
    cleaned_map = move_blocks(disk_map)
    advent.submit(1, checksum(cleaned_map))


def checksum(disk_map: list[int]):
    return sum([idx * id for idx, id in enumerate(disk_map) if id >= 0])


def move_blocks(disk_map: list[int]):
    last_block = len(disk_map) - 1
    while disk_map[last_block] == -1:
        last_block -= 1
    for index in range(len(disk_map)):
        if index >= last_block:
            break
        if disk_map[index] == -1:
            disk_map[index] = disk_map[last_block]
            disk_map[last_block] = -1
            while disk_map[last_block] == -1:
                last_block -= 1

    return disk_map[: last_block + 1]


def get_disk_map(input: str):
    disk_map = []
    id = 0
    is_file = True
    for val in input:
        if is_file:
            disk_map.extend([id] * int(val))
            id += 1
        else:
            disk_map.extend([-1] * int(val))
        is_file = not is_file

    return disk_map


if __name__ == "__main__":
    main()
