from enum import Enum
from typing import List, AnyStr, Tuple, Optional, Set


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


Coord = Tuple[int, int]


def turn_right(direction: Direction) -> Direction:
    new_direction = {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP,
    }
    return new_direction[direction]


def next_position(direction: Direction, i: int, j: int) -> Coord:
    if direction == Direction.UP:
        return i - 1, j
    if direction == Direction.RIGHT:
        return i, j + 1
    if direction == Direction.DOWN:
        return i + 1, j
    if direction == Direction.LEFT:
        return i, j - 1


def is_out_of_bounds(i: int, j: int, h: int, w: int) -> bool:
    return i < 0 or i >= h or j < 0 or j >= w


class Map(object):
    def __init__(self, lines: List[AnyStr]):
        self.lines = lines
        self.height = len(lines)
        self.width = len(self.lines[0])

        # Starting positions
        self.start = None

        for i in range(len(lines)):
            j = lines[i].find('^')
            if j != -1:
                self.start = (i, j)
                break
        else:
            raise Exception('No starting position found!')

    def is_out_of_bounds(self, i, j):
        return i < 0 or i >= self.height or j < 0 or j >= self.width

    def is_obstacle(self, i: int, j: int) -> bool:
        return not self.is_out_of_bounds(i, j) and self.lines[i][j] == '#'

    def has_obstacles_ahead(self, direction: Direction,
                            position: Coord) -> bool:
        i, j = next_position(direction, *position)
        while not self.is_out_of_bounds(i, j):
            if self.lines[i][j] == "#": return True
            i, j = next_position(direction, i, j)
        return False

    def walk(self, direction: Direction, start: Coord,
             extra_obstacle: Optional[Coord] = None) -> Tuple[
        int, int, Direction]:
        i, j = start

        while True:
            yield i, j, direction

            next_i, next_j = next_position(direction, i, j)
            if self.is_out_of_bounds(next_i, next_j):
                return

            while self.is_obstacle(next_i, next_j) or (
            next_i, next_j) == extra_obstacle:
                direction = turn_right(direction)
                next_i, next_j = next_position(direction, i, j)

            i, j = next_i, next_j

    def get_path(self) -> Set[Coord]:
        direction = Direction.UP
        visited = set()

        for i, j, direction in self.walk(direction, self.start):
            if (i, j) not in visited:
                visited.add((i, j))

        return visited

    def is_loop(self, obstacle: Coord) -> bool:
        states = set()
        for i, j, direction in self.walk(Direction.UP, self.start, obstacle):
            if (i, j, direction) in states:
                return True
            states.add((i, j, direction))
        return False



puzzle = Map([x.strip() for x in open('p6.txt').readlines()])
path = puzzle.get_path()
print(f'Positions visited: {len(path)}')

loops = 0
for potential_obstacle in path:
    if puzzle.is_loop(potential_obstacle):
        loops += 1
print(f'Loops: {loops}')