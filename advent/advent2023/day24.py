from collections import Counter
from itertools import combinations
from typing import cast

from advent.utils.utils import Advent

advent = Advent(24, 2023)


def main():
    lines = advent.get_input_lines()
    stones = get_stones(lines)

    total = 0
    for s1, s2 in combinations(stones, 2):
        if intersect_in_area(*s1, *s2, 200000000000000, 400000000000000):
            total += 1
    advent.submit(1, total)

    answers = Counter()
    count = 0
    for s1, s2, s3 in combinations(stones, 3):
        answers[solve([s1, s2, s3])] += 1
        count += 1
        if count > 100:
            break
    advent.submit(2, answers.most_common(1)[0][0])


def solve(stones: list[tuple[tuple[int, ...], tuple[int, ...]]]) -> int:
    """
    Solution from
    https://github.com/mebeim/aoc/blob/master/2023/solutions/day24.py
    """
    (a, va), (b, vb), (c, vc) = stones[:3]

    # Let our 6 unknowns be: p = (x, y, z) and v = (vx, vy, vz)
    # Solve the linear system of 6 equations given by:
    #
    #   (p - a) X (v - va) == (p - b) X (v - vb)
    #   (p - a) X (v - va) == (p - c) X (v - vc)
    #
    # Where X represents the vector cross product.

    A1, B1 = get_equations(a, va, b, vb)
    A2, B2 = get_equations(a, va, c, vc)
    A = A1 + A2
    B = B1 + B2

    # Could also use fractions.Fraction to avoid rounding mistakes
    x = matrix_mul(matrix_inverse(A), B)
    return sum(map(round, x[:3]))


def get_equations(
    a: tuple[int, ...],
    va: tuple[int, ...],
    b: tuple[int, ...],
    vb: tuple[int, ...],
) -> tuple[list[list[float]], list[float]]:
    # Return the coefficient matrix (A) and the constant terms vector (B) for
    # the 3 equations given by:
    #
    #   (p - a) X (v - va) == (p - b) X (v - vb)

    dx, dy, dz = vector_diff(a, b)
    dvx, dvy, dvz = vector_diff(va, vb)

    A = [
        [0, -dvz, dvy, 0, -dz, dy],
        [dvz, 0, -dvx, dz, 0, -dx],
        [-dvy, dvx, 0, -dy, dx, 0],
    ]

    B = [
        b[1] * vb[2] - b[2] * vb[1] - (a[1] * va[2] - a[2] * va[1]),
        b[2] * vb[0] - b[0] * vb[2] - (a[2] * va[0] - a[0] * va[2]),
        b[0] * vb[1] - b[1] * vb[0] - (a[0] * va[1] - a[1] * va[0]),
    ]

    return cast(list[list[float]], A), cast(list[float], B)


def matrix_transpose(m: list[list[float]]) -> list[list[float]]:
    return list(map(list, zip(*m)))


def matrix_minor(m: list[list[float]], i: int, j: int) -> list[list[float]]:
    return [row[:j] + row[j + 1 :] for row in (m[:i] + m[i + 1 :])]


def matrix_det(m: list[list[float]]) -> float:
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * matrix_det(matrix_minor(m, 0, c))

    return determinant


def matrix_inverse(m: list[list[float]]) -> list[list[float]]:
    determinant = matrix_det(m)
    cofactors = []

    for r in range(len(m)):
        row = []

        for c in range(len(m)):
            minor = matrix_minor(m, r, c)
            row.append(((-1) ** (r + c)) * matrix_det(minor))

        cofactors.append(row)

    cofactors = matrix_transpose(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] /= determinant

    return cofactors


def matrix_mul(m: list[list[float]], vec: list[float]) -> list[float]:
    res = []
    for row in m:
        res.append(sum(r * v for r, v in zip(row, vec)))
    return res


def vector_diff(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def intersect_in_area(
    p1: tuple[int, int, int],
    v1: tuple[int, int, int],
    p2: tuple[int, int, int],
    v2: tuple[int, int, int],
    minx: int,
    maxx: int,
) -> bool:
    ip = line_intersection(p1, v1, p2, v2)
    if ip is None:
        return False

    x, y = ip
    if x < minx or x > maxx or y < minx or y > maxx:
        return False

    dx1 = x - p1[0]
    dx2 = x - p2[0]
    dy1 = y - p1[1]
    dy2 = y - p2[1]
    if dx1 * v1[0] < 0 or dx2 * v2[0] < 0 or dy1 * v1[1] < 0 or dy2 * v2[1] < 0:
        return False

    return True


def get_stones(
    lines: list[str],
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    stones = []
    for line in lines:
        left, right = line.split("@")
        pos = tuple([int(c.strip()) for c in left.strip().split(",")])
        v = tuple([int(c.strip()) for c in right.strip().split(",")])
        stones.append((pos, v))
    return stones


def det(a: tuple[int, int], b: tuple[int, int]) -> int:
    a0, a1 = a
    b0, b1 = b
    return a0 * b1 - a1 * b0


def line_intersection(
    p1: tuple[int, int, int],
    v1: tuple[int, int, int],
    p2: tuple[int, int, int],
    v2: tuple[int, int, int],
) -> tuple[float, float] | None:
    px1, py1, _ = p1
    px2, py2, _ = p2
    vx1, vy1, _ = v1
    vx2, vy2, _ = v2
    xdiff = (-vx1, -vx2)
    ydiff = (-vy1, -vy2)
    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (
        det((px1, py1), (px1 + vx1, py1 + vy1)),
        det((px2, py2), (px2 + vx2, py2 + vy2)),
    )
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


if __name__ == "__main__":
    main()
