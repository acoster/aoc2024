import itertools
from enum import Enum
from typing import List, Any


def batched(iterable, n, *, strict=False):
    if hasattr(itertools, 'batched'):
        return itertools.batched(iterable, n, strict=strict)

    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError('batched(): incomplete batch')
        yield batch


class Coord(object):
    """2D coordinates."""

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


class Direction(Enum):
    UP = Coord(-1, 0)
    RIGHT = Coord(0, 1)
    DOWN = Coord(1, 0)
    LEFT = Coord(0, -1)

    def turn_right(self):
        new_direction = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }
        return new_direction[self]

    def turn_left(self):
        new_direction = {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
        }
        return new_direction[self]

