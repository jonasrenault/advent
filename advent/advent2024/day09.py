from advent.utils.utils import Advent

advent = Advent(9, 2024)


def main():
    lines = advent.get_input_lines()
    disk_map = get_disk_map(lines[0])
    cleaned_map = move_blocks(disk_map)
    advent.submit(1, checksum(cleaned_map))

    files, free = get_disk_map2(lines[0])
    move2(files, free)
    advent.submit(2, checksum2(files))


def checksum(disk_map: list[int]) -> int:
    return sum([idx * id for idx, id in enumerate(disk_map) if id >= 0])


def move_blocks(disk_map: list[int]) -> list[int]:
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


def get_disk_map(input: str) -> list[int]:
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


def checksum2(files: dict[int, list[int]]) -> int:
    total = 0
    for id, blocks in files.items():
        total += sum([id * idx for idx in blocks])
    return total


def move2(files: dict[int, list[int]], free: dict[int, int]):
    id = max(files.keys())
    while id > 1:
        blocks = len(files[id])
        file_start = files[id][0]
        possible = [
            idx for idx, length in free.items() if blocks <= length and idx < file_start
        ]
        if possible:
            # free up file space, joining with possible left or right free space
            join_to = [
                idx
                for idx, length in free.items()
                if idx < file_start and idx + length == file_start
            ]
            free_idx = join_to[0] if join_to else file_start
            free[free_idx] = free.get(free_idx, 0) + blocks
            right_join_idx = free_idx + free[free_idx]
            if right_join_idx in free:
                free[free_idx] += free[right_join_idx]
                del free[right_join_idx]

            # update file blocks and update free block space
            move_to = min(possible)
            files[id] = [move_to + i for i in range(blocks)]
            if blocks < free[move_to]:
                free[move_to + blocks] = free[move_to] - blocks
            del free[move_to]
        id -= 1


def get_disk_map2(input: str) -> tuple[dict[int, list[int]], dict[int, int]]:
    files = dict()
    free = dict()
    id = 0
    index = 0
    is_file = True
    for val in input:
        if is_file:
            files[id] = [index + i for i in range(int(val))]
            id += 1
        elif int(val) > 0:
            free[index] = int(val)
        index += int(val)
        is_file = not is_file

    return files, free


if __name__ == "__main__":
    main()
