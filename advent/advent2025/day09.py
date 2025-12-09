from itertools import combinations
from typing import TypeAlias, cast

from advent.utils import Advent

advent = Advent(9, 2025)

Point: TypeAlias = tuple[int, int]
Edge: TypeAlias = tuple[int, int, int, int]


def main():
    lines = advent.get_input_lines()
    tiles = [cast(Point, tuple(map(int, line.split(",")))) for line in lines]

    areas = [get_area(a, b) for a, b in combinations(tiles, 2)]
    advent.submit(1, max(areas))

    advent.submit(2, max_area_inside(tiles))


def max_area_inside(tiles: list[Point]) -> int:
    """
    Get the maximum area of any rectangle that is fully inside the polygon,
    i.e. which does not cross any of the edges.

    This only works because the input data represents a circle with a hollow
    line across the middle, hence the maximum rectangle is one that is fully
    contained in the polygon. This solution would not work for an other input
    shape.

    The input data looks like this:

                        ##
                      #####
                    #########
                  #############
                            ###
                 #############
                   #########
                    ######
                      ##

    Args:
        tiles (list[Point]): the list of red tiles.

    Returns:
        int: the maximum area of valid rectangles.
    """
    edges = get_edges(tiles)
    max_area = 0
    for a, b in combinations(tiles, 2):
        x1 = min(a[0], b[0])
        x2 = max(a[0], b[0])
        y1 = min(a[1], b[1])
        y2 = max(a[1], b[1])
        area = get_area(a, b)
        if area > max_area:
            if not intersects((x1, y1, x2, y2), edges):
                max_area = area

    return max_area


def intersects(rectangle: Edge, edges: list[Edge]) -> bool:
    """
    Returns True if the rectangle intersects any of the edges.

    Args:
        rectangle (Edge): the rectangle as Xmin, Ymin, Xmax Ymax.
        edges (list[Edge]): the list of edges for the polygon.

    Returns:
        bool: True if the rectangle intersects any edge.
    """
    x1, y1, x2, y2 = rectangle
    for ex1, ey1, ex2, ey2 in edges:
        if x1 < ex2 and x2 > ex1 and y1 < ey2 and y2 > ey1:
            return True
    return False


def get_area(a: Point, b: Point) -> int:
    x1, y1 = a
    x2, y2 = b
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def get_edges(tiles: list[Point]) -> list[Edge]:
    edges = []
    x1, y1 = tiles[0]
    for x2, y2 in tiles[1:] + [(x1, y1)]:
        edges.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
        x1, y1 = x2, y2
    return edges


if __name__ == "__main__":
    main()
