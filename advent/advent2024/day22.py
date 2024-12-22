from collections import deque

from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(22, 2024)


def main():
    lines = advent.get_input_lines()
    secrets = list(map(int, lines))

    evolved = generate_random_secrets(secrets)
    advent.submit(1, sum(evolved))

    buyer_prices = get_buyer_prices(secrets)
    sequences = set()
    for buyer in buyer_prices:
        sequences.update(buyer.keys())

    best_bananas = 0
    for sequence in tqdm(sequences):
        bananas = 0
        for buyer in buyer_prices:
            bananas += buyer.get(sequence, 0)
        if bananas > best_bananas:
            best_bananas = bananas

    advent.submit(2, best_bananas)


def get_buyer_prices(
    secrets: list[int], steps: int = 2001
) -> list[dict[tuple[int, ...], int]]:
    buyer_prices = []
    for secret in tqdm(secrets):
        previous = None
        changes: deque[int] = deque([])
        prices: dict[tuple[int, ...], int] = dict()
        for _ in range(steps):
            price = int(str(secret)[-1])
            if previous is not None:
                changes.append(price - previous)
                if len(changes) > 4:
                    changes.popleft()
                if len(changes) == 4 and tuple(changes) not in prices:
                    prices[tuple(changes)] = price
            previous = price
            secret = evolve(secret)
        buyer_prices.append(prices)
    return buyer_prices


def generate_random_secrets(secrets: list[int], steps: int = 2000) -> list[int]:
    evolved = []
    for secret in secrets:
        for _ in range(steps):
            secret = evolve(secret)
        evolved.append(secret)
    return evolved


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
