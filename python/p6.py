from collections import namedtuple
from enum import Enum
from typing import List, AnyStr, Tuple, Optional, Set, Iterator


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def turn(self):
        new_direction = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }
        return new_direction[self]


Coord = namedtuple("Coord", ["i", "j"])


def next_position(direction: Direction, p: Coord) -> Coord:
    if direction == Direction.UP:
        return Coord(p.i - 1, p.j)
    if direction == Direction.RIGHT:
        return Coord(p.i, p.j + 1)
    if direction == Direction.DOWN:
        return Coord(p.i + 1, p.j)
    if direction == Direction.LEFT:
        return Coord(p.i, p.j - 1)


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
                self.start = Coord(i, j)
                break
        else:
            raise Exception('No starting position found!')

    def is_out_of_bounds(self, p: Coord) -> bool:
        return p.i < 0 or p.i >= self.height or p.j < 0 or p.j >= self.width

    def is_obstacle(self, p: Coord) -> bool:
        return not self.is_out_of_bounds(p) and self.lines[p.i][p.j] == '#'

    def walk(self, direction: Direction, start: Coord,
             extra_obstacle: Optional[Coord] = None) -> Iterator[Tuple[
        Coord, Direction]]:
        pos = start

        while True:
            yield pos, direction
            np = next_position(direction, pos)
            if self.is_out_of_bounds(np):
                return

            while self.is_obstacle(np) or np == extra_obstacle:
                direction = direction.turn()
                np = next_position(direction, pos)

            pos = np

    def get_path(self) -> Set[Coord]:
        return {x[0] for x in self.walk(Direction.UP, self.start)}

    def is_loop(self, obstacle: Coord) -> bool:
        states = set()
        for pos, direction in self.walk(Direction.UP, self.start, obstacle):
            if (pos, direction) in states:
                return True
            states.add((pos, direction))
        return False


if __name__ == '__main__':
    puzzle = Map([x.strip() for x in open('p6.txt').readlines()])
    path = puzzle.get_path()
    print(f'Positions visited: {len(path)}')

    loops = 0
    for potential_obstacle in path:
        if puzzle.is_loop(potential_obstacle):
            loops += 1
    print(f'Loops: {loops}')
