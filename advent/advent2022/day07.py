import re
from collections import defaultdict
from pathlib import Path

from advent2022.utils.utils import Advent

advent = Advent(7)


def main():
    lines = advent.get_input_lines()
    contents = get_tree(lines)
    sizes = {}
    used = get_size(Path("/"), contents, sizes)
    advent.submit(1, sum([v for v in sizes.values() if v <= 100000]))

    total_dsp = 70000000
    needed = 30000000 - (total_dsp - used)
    advent.submit(2, min(filter(lambda x: x > needed, sizes.values())))


def get_tree(lines: str) -> dict[Path, list[Path | tuple[str, int]]]:
    contents: defaultdict[Path, list[Path | tuple[str, int]]] = defaultdict(list)
    cwd = Path("/")
    for line in lines:
        m = re.match(r"(\d+) (.+)", line)

        if line == "$ cd ..":
            cwd = cwd.parent
        elif line == "$ cd /":
            cwd = Path("/")
        elif line.startswith("$ cd "):
            cwd = cwd / line[5:]
        elif line.startswith("dir"):
            contents[cwd].append(cwd / line[4:])
        elif m is not None:
            size = m.group(1)
            file = str(m.group(2))
            contents[cwd].append((file, int(size)))
    return contents


def get_size(
    dir: Path,
    contents: dict[Path, list[Path | tuple[str, int]]],
    sizes: dict[Path, int],
) -> int:
    """
    Given a directory path, compute it's size based on the contents tree.

    Parameters
    ----------
    dir : Path
        the directory path to compute the size for.
    contents : Dict[Path, List[Path  |  Tuple[str, int]]]
        the contents tree
    sizes : Dict[Path, int]
        A dict containing sizes for the given dir and its sub directories

    Returns
    -------
    int
        the size for the given directory
    """
    if dir in sizes:
        return sizes[dir]
    size = sum(
        [
            f[1] if isinstance(f, tuple) else get_size(f, contents, sizes)
            for f in contents[dir]
        ]
    )
    sizes[dir] = size
    return size


if __name__ == "__main__":
    main()
