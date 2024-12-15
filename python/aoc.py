import itertools
from enum import Enum
from typing import List, Any


def batched(iterable, n):
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        yield batch


class Coord(object):
    """2D coordinates."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def in_bounds(self, grid: List[Any]) -> bool:
        return 0 <= self.y < len(grid) and 0 <= self.x < len(grid[0])

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"


class Direction(Enum):
    UP = Coord(0, -1)
    RIGHT = Coord(1, 0)
    DOWN = Coord(0, 1)
    LEFT = Coord(-1, 0)

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

