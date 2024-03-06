import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from advent.utils.utils import Advent

advent = Advent(20, 2021)


def main():
    lines = advent.get_input_lines()
    algo = [1 if c == "#" else 0 for c in lines[0]]
    image = np.array(
        [[1 if c == "#" else 0 for c in line] for line in lines[2:]], dtype=int
    )

    image_2 = enhance(image, algo, 2)
    advent.submit(1, np.count_nonzero(image_2))

    image_50 = enhance(image_2, algo, 48)
    advent.submit(2, np.count_nonzero(image_50))


def enhance(
    image: npt.NDArray[np.int_], algo: list[int], steps: int
) -> npt.NDArray[np.int_]:
    for step in tqdm(range(steps)):
        image = convolute(image, algo, step % 2)
    return image


def convolute(
    image: npt.NDArray[np.int_], algo: list[int], empty_space: int = 0
) -> npt.NDArray[np.int_]:
    padded = np.pad(
        image,
        ((3, 3), (3, 3)),
        "constant",
        constant_values=((empty_space, empty_space), (empty_space, empty_space)),
    )
    maxr = padded.shape[0] - 1
    maxc = padded.shape[1] - 1
    new_image = np.zeros((maxr - 1, maxc - 1), dtype=int)
    for r in range(1, maxr):
        for c in range(1, maxc):
            kernel = padded[r - 1 : r + 2, c - 1 : c + 2]
            idx = int("".join(map(str, kernel.flatten().tolist())), 2)
            new_image[r - 1, c - 1] = algo[idx]
    return new_image


if __name__ == "__main__":
    main()
