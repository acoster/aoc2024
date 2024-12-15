import copy

from aoc import Coord, Direction
from typing import List, AnyStr, Dict

class Puzzle(object):
    def __init__(self, lines: List[AnyStr]):
        self.height = len(lines)
        self.width = len(lines[0])
        self.map = dict()
        self.robot = None

        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == '@':
                    self.robot = Coord(x, y)
                self.map[Coord(x, y)] = lines[y][x]

    def print_map(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.map[Coord(x, y)], end='')
            print()
        print()

    def move(self, direction: Direction) -> None:
        result = self.compute_move(self.robot, direction)
        if len(result) == 0: return
        for pos, value in result.items():
            self.map[pos] = value
            if value == '@':
                self.map[self.robot] = '.'
                self.robot = pos


    def compute_move(self, origin: Coord, direction: Direction) -> Dict[Coord, AnyStr]:
        # Don't try moving nothingness or walls.
        if self.map[origin] == '.' or self.map[origin] == '#':
            return dict()

        np = origin + direction.value
        # Nothing to do if next position is a wall
        if self.map[np] == '#': return dict()
        if self.map[np] == '.': return {np: self.map[origin]}

        changes = self.compute_move(np, direction)
        if len(changes) == 0: return dict()
        changes[np] = self.map[origin]
        changes[origin] = '.'
        return changes

if __name__ == '__main__':
    l = [x.strip() for x in open('p15.txt').readlines()]
    b = l.index('')
    puzzle = Puzzle(l[:b])

    for line in l[b+1:]:
        for c in line:
            puzzle.move(Direction.from_char(c))

    total = 0
    for pos, value in puzzle.map.items():
        if value == 'O':
            total += pos.x + 100 * pos.y

    print(f'The total sum is {total}')