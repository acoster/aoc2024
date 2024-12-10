from typing import List, Any


class Coord(object):
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j

    def in_bounds(self, grid: List[Any]) -> bool:
        return 0 <= self.i < len(grid) and 0 <= self.j < len(grid[0])

    def __add__(self, other):
        return Coord(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Coord(self.i - other.i, self.j - other.j)

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))

    def __repr__(self):
        return f"Coord({self.i}, {self.j})"


UP = Coord(-1, 0)
RIGHT = Coord(0, 1)
DOWN = Coord(0, -1)
LEFT = Coord(1, 0)