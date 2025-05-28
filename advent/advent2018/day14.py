from advent.utils import Advent

advent = Advent(14, 2018)


def main():
    lines = advent.get_input_lines()

    advent.submit(1, "".join(map(str, run(int(lines[0]))[-10:])))
    advent.submit(2, find(int(lines[0])))


def find(recipes: int):
    score = [3, 7]
    e1, e2 = 0, 1
    targetscores = tuple(map(int, str(recipes)))
    targetlen = len(targetscores)
    checked = 0
    size = 0
    while True:
        s = str(score[e1] + score[e2])
        size += len(s)
        score.extend(int(c) for c in s)
        e1 = (e1 + 1 + score[e1]) % len(score)
        e2 = (e2 + 1 + score[e2]) % len(score)

        while checked <= size - targetlen:
            for t, r in zip(targetscores, score[checked:]):
                if t != r:
                    break
            else:
                return checked

            checked += 1


def run(recipes: int):
    score = [3, 7]
    e1, e2 = 0, 1
    while len(score) < recipes + 10:
        score.extend(int(c) for c in str(score[e1] + score[e2]))
        e1 = (e1 + 1 + score[e1]) % len(score)
        e2 = (e2 + 1 + score[e2]) % len(score)
    return score


if __name__ == "__main__":
    main()
