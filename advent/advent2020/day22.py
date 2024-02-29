from advent.utils.utils import Advent

advent = Advent(22, 2020)


def main():
    lines = advent.get_input_lines()
    decks = get_decks(lines)

    deck1, deck2 = play_game(*decks)
    deck = deck1
    if len(deck2) > 0:
        deck = deck2
    advent.submit(1, sum([x * (len(deck) - i) for i, x in enumerate(deck)]))

    deck1, deck2 = play_recursive_game(*decks)
    deck = deck1
    if len(deck2) > 0:
        deck = deck2
    advent.submit(2, sum([x * (len(deck) - i) for i, x in enumerate(deck)]))


def play_recursive_game(
    deck1: tuple[int, ...], deck2: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    history = set()
    while len(deck1) > 0 and len(deck2) > 0:
        game = ",".join(map(str, deck1)) + "|" + ",".join(map(str, deck2))
        if game in history:
            return ((1,), ())
        history.add(game)
        deck1, deck2 = play_recursive_round(deck1, deck2)

    return deck1, deck2


def play_recursive_round(
    deck1: tuple[int, ...], deck2: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left = deck1[0]
    right = deck2[0]

    if len(deck1[1:]) >= left and len(deck2[1:]) >= right:
        dl, _ = play_recursive_game(deck1[1 : left + 1], deck2[1 : right + 1])
        if len(dl) == 0:  # Player2 won
            return deck1[1:], deck2[1:] + (right, left)
        return deck1[1:] + (left, right), deck2[1:]
    else:  # regular round
        if left > right:
            return deck1[1:] + (left, right), deck2[1:]
        return deck1[1:], deck2[1:] + (right, left)


def play_game(
    deck1: tuple[int, ...], deck2: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    while len(deck1) > 0 and len(deck2) > 0:
        deck1, deck2 = play_round(deck1, deck2)

    return deck1, deck2


def play_round(
    deck1: tuple[int, ...], deck2: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """
    Play a round.

    Args:
        decks (tuple[deque[int], deque[int]]): decks
    """
    left = deck1[0]
    right = deck2[0]
    if left > right:
        return deck1[1:] + (left, right), deck2[1:]
    return deck1[1:], deck2[1:] + (right, left)


def get_decks(lines: list[str]) -> tuple[tuple[int, ...], ...]:
    """
    Read decks.

    Args:
        lines (list[str]): input lines

    Returns:
        tuple[tuple[int, ...], ...]: decks
    """
    decks = []
    deck: list[int] = []
    for line in lines[1:]:
        if not line:
            continue
        if line.startswith("Player"):
            decks.append(tuple(deck))
            deck = []
        else:
            deck.append(int(line))
    decks.append(tuple(deck))
    return tuple(decks)


if __name__ == "__main__":
    main()
