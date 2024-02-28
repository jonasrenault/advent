from advent2022.utils.utils import Advent

advent = Advent(10)


def main():
    lines = advent.get_input_lines()
    signals = get_signals(lines)
    advent.submit(1, sum([i * signals[i - 1] for i in range(20, 221, 40)]))

    rows = draw_pixels(signals)
    for row in rows:
        print(" ".join(row))
    advent.submit(2, "ZKGRKGRK")


def draw_pixels(signals: list[int]) -> list[list[str]]:
    rows = []
    for row in range(6):
        pixels = []
        for pixel in range(1, 41):
            cycle = 40 * row + pixel
            if signals[cycle - 1] <= pixel <= signals[cycle - 1] + 2:
                pixels.append("#")
            else:
                pixels.append(".")
        rows.append(pixels)
    return rows


def get_signals(lines: list[str]) -> list[int]:
    signals = [1]
    for line in lines:
        signals.append(signals[-1])
        if line != "noop":
            signals.append(int(line[5:]) + signals[-1])
    return signals


if __name__ == "__main__":
    main()
