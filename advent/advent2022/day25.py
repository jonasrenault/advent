from advent.utils.utils import Advent

advent = Advent(25, 2022)


def main():
    lines = advent.get_input_lines()
    advent.submit(1, dec_to_snafu(sum([snafu_to_dec(line) for line in lines])))


def dec_to_snafu(num: int) -> str:
    # get base 5 repr
    if num == 0:
        return "0"
    nums = []
    while num:
        num, r = divmod(num, 5)
        nums.append(str(r))

    # replace 3, 4 and 5s
    for i in range(len(nums)):
        if int(nums[i]) > 2:

            if nums[i] == "3":
                nums[i] = "="
            elif nums[i] == "4":
                nums[i] = "-"
            elif nums[i] == "5":
                nums[i] = "0"

            if i + 1 < len(nums):
                nums[i + 1] = str(int(nums[i + 1]) + 1)
            else:
                nums.append("1")

    return "".join(reversed(nums))


def snafu_to_dec(num: str) -> int:
    res = 0
    for exp, val in enumerate(num[::-1]):
        if val == "=":
            factor = -2
        elif val == "-":
            factor = -1
        else:
            factor = int(val)
        res += factor * pow(5, exp)
    return int(res)


if __name__ == "__main__":
    main()
