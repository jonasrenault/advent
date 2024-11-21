import numpy as np
import numpy.typing as npt
import pytest

from advent.utils.algos import neighbors, neighbors8


@pytest.fixture
def grid() -> npt.NDArray[np.int_]:
    return np.zeros((50, 100))


@pytest.fixture
def grid_list() -> list[list[int]]:
    return [[0 for _ in range(100)] for _ in range(50)]


def test_neighbors(grid: npt.NDArray[np.int_], grid_list: list[list[int]]):
    it = neighbors(grid, (15, 20))

    assert next(it) == (14, 20)
    assert next(it) == (15, 19)
    assert next(it) == (15, 21)
    assert next(it) == (16, 20)

    assert list(neighbors(grid, (49, 20))) == [(48, 20), (49, 19), (49, 21)]
    assert list(neighbors(grid, (0, 0))) == [(0, 1), (1, 0)]

    it = neighbors(grid_list, (15, 20))

    assert next(it) == (14, 20)
    assert next(it) == (15, 19)
    assert next(it) == (15, 21)
    assert next(it) == (16, 20)

    assert list(neighbors(grid_list, (49, 20))) == [(48, 20), (49, 19), (49, 21)]
    assert list(neighbors(grid_list, (0, 0))) == [(0, 1), (1, 0)]


def test_neighbors8(grid: npt.NDArray[np.int_], grid_list: list[list[int]]):
    it = neighbors8(grid, (15, 20))

    assert next(it) == (14, 19)
    assert next(it) == (14, 20)
    assert next(it) == (14, 21)
    assert next(it) == (15, 19)
    assert next(it) == (15, 21)
    assert next(it) == (16, 19)
    assert next(it) == (16, 20)
    assert next(it) == (16, 21)

    assert list(neighbors8(grid, (49, 20))) == [
        (48, 19),
        (48, 20),
        (48, 21),
        (49, 19),
        (49, 21),
    ]
    assert list(neighbors8(grid, (0, 0))) == [(0, 1), (1, 0), (1, 1)]

    it = neighbors8(grid_list, (15, 20))

    assert next(it) == (14, 19)
    assert next(it) == (14, 20)
    assert next(it) == (14, 21)
    assert next(it) == (15, 19)
    assert next(it) == (15, 21)
    assert next(it) == (16, 19)
    assert next(it) == (16, 20)
    assert next(it) == (16, 21)

    assert list(neighbors8(grid_list, (49, 20))) == [
        (48, 19),
        (48, 20),
        (48, 21),
        (49, 19),
        (49, 21),
    ]
    assert list(neighbors8(grid_list, (0, 0))) == [(0, 1), (1, 0), (1, 1)]
