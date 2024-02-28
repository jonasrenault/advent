from advent2022.utils.utils import Advent

advent = Advent(20)


def main():
    lines = advent.get_input_lines()
    file = list(map(int, lines))
    advent.submit(1, mix(file))
    advent.submit(2, mix2(list(map(int, lines))))


def mix2(file: list[int]) -> int:
    nums = [811589153 * c for c in file]
    size = len(nums)
    orders = list(range(size))

    for i in range(10):
        for i in range(size):
            pos = orders.index(i)
            element = nums[pos]
            new_pos = (pos + element) % (size - 1)

            nums.insert(new_pos, nums.pop(pos))
            orders.insert(new_pos, orders.pop(pos))

    zero_i = nums.index(0)
    return sum([nums[(i + zero_i) % size] for i in range(1000, 4000, 1000)])


def mix(file: list[int]) -> int:
    size = len(file)
    orders = list(range(size))

    for i in range(size):
        pos = orders.index(i)
        element = file[pos]
        new_pos = (pos + element) % (size - 1)

        file.insert(new_pos, file.pop(pos))
        orders.insert(new_pos, orders.pop(pos))

    zero_i = file.index(0)
    return sum([file[(i + zero_i) % size] for i in range(1000, 4000, 1000)])


if __name__ == "__main__":
    main()
