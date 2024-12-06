from enum import Enum
from typing import List, AnyStr, Tuple

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4





def turn_right(direction: Direction) -> Direction:
    new_direction = {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP,
    }
    return new_direction[direction]

def next_position(direction: Direction, i: int, j: int) -> Tuple[int, int]:
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
        self.i = 0
        self.j = 0

        for i in range(len(lines)):
            j = lines[i].find('^')
            if j != -1:
                self.i = i
                self.j = j
                break
        else:
            raise Exception('No starting position found!')

    def is_out_of_bounds(self, i, j):
        return i < 0 or i >= self.height or j < 0 or j >= self.width

    def is_obstacle(self, i: int, j: int) -> bool:
        return self.lines[i][j] == '#'

    def has_obstacles_ahead(self, direction: Direction, i: int, j: int ) -> bool:
        i, j =  next_position(direction, i, j)
        while not self.is_out_of_bounds(i, j):
            if self.lines[i][j] == "#": return True
            i, j = next_position(direction, i, j)
        return False


    def count_positions(self) -> int:
        direction = Direction.UP
        i = self.i
        j = self.j

        visited = set()

        while True:
            if (i, j) not in visited:
                visited.add((i, j))

            next_i, next_j = next_position(direction, i, j)
            if self.is_out_of_bounds(next_i, next_j):
                return len(visited)

            if self.is_obstacle(next_i, next_j):
                direction = turn_right(direction)
            else:
                i, j = next_i, next_j

    def count_loops(self) -> int:
        # Will do once not so busy. TL;DR: for each step, check if there's an
        # obstacle to the (relative) right, and if so, check if adding an
        # obstacle ahead causes a loop.
        return 0

puzzle = Map([x.strip() for x in  open('p6.txt').readlines()])
result = puzzle.count_positions()
print(f'Positions visited: {result}')