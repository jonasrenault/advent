from math import ceil, sqrt

from advent.utils import Advent

advent = Advent(25, 2020)


def main():
    lines = advent.get_input_lines()
    card_pkey = lines[0]
    door_pkey = lines[1]
    card_step = bsgs(7, int(card_pkey), 20201227)
    # door_step = bsgs(7, int(door_pkey), 20201227)
    card_secret_key = pow(int(door_pkey), card_step, 20201227)
    # door_secret_key = pow(int(card_pkey), door_step, 20201227)
    advent.submit(1, card_secret_key)


def bsgs(base, n, p):
    m = ceil(sqrt(p))
    table = {pow(base, i, p): i for i in range(m)}
    inv = pow(
        base, (p - 2) * m, p
    )  # base^(-m) mod p == base^(m*(p-2)) assuming p is prime
    res = None

    for i in range(m):
        y = (n * pow(inv, i, p)) % p
        if y in table:
            res = i * m + table[y]
            break

    return res


if __name__ == "__main__":
    main()
