from advent.utils.utils import Advent

advent = Advent(1, 2021)


def main():
    lines = advent.get_input_lines()
    depths = [int(line) for line in lines]
    pos_diffs = [b - a for a, b in zip(depths, depths[1:]) if b - a > 0]
    advent.submit(1, len(pos_diffs))

    windows = [depths[i] + depths[i + 1] + depths[i + 2] for i in range(len(depths) - 2)]
    window_diffs = [b - a for a, b in zip(windows, windows[1:]) if b - a > 0]
    advent.submit(2, len(window_diffs))


if __name__ == "__main__":
    main()
