from advent.utils.utils import Advent

advent = Advent(22, 2024)


def main():
    lines = advent.get_input_lines()
    secrets = list(map(int, lines))
    evolved = []
    for secret in secrets:
        for _ in range(2000):
            secret = evolve(secret)
        evolved.append(secret)

    advent.submit(1, sum(evolved))


def evolve(secret: int) -> int:
    secret ^= secret * 64
    secret %= 16777216
    secret ^= int(secret / 32)
    secret %= 16777216
    secret ^= secret * 2048
    secret %= 16777216
    return secret


if __name__ == "__main__":
    main()
