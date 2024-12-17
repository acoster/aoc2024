import copy

from aoc import Coord, Direction
from typing import List, AnyStr, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Move(object):
    target: Coord
    source: Optional[Coord]


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

    def score(self):
        total = 0
        for pos, value in self.map.items():
            if value == 'O' or value == '[':
                total += pos.x + 100 * pos.y
        return total

    def print_map(self):
        print(' ', end='')
        for i in range(self.width):
            print(i % 10, end='')
        print()

        for y in range(self.height):
            print(y%10, end='')
            for x in range(self.width):
                print(self.map[Coord(x, y)], end='')
            print()
        print()

    def move(self, direction: Direction) -> None:
        result = self.compute_move(self.robot, None, direction)
        if len(result) == 0: return
        snapshot = dict(self.map)
        moves = dict()
        for move in result:
            if move.target not in moves:
                moves[move.target] = move
                continue
            if move.source is not None and moves[move.target].source is None:
                moves[move.target] = move

        for move in moves.values():
            if move.source is None:
                self.map[move.target] = '.'
                continue
            if move.source == self.robot:
                self.robot = move.target
            self.map[move.target] = snapshot[move.source]

    def compute_move(self, pos: Coord, previous: Optional[Coord], direction: Direction) -> List[Move]:
        if self.map[pos] == '#': return []
        if self.map[pos] == '.':
            assert previous is not None
            return [Move(pos, previous)]

        np = pos + direction.value

        wide_moves = []
        if direction == Direction.UP or direction == Direction.DOWN:
            if self.map[np] == '[' and self.map[pos] != '[':
                wide_moves = self.compute_move(np + Coord(1, 0), None, direction)
                if len(wide_moves) == 0: return []
            elif self.map[np] == ']' and self.map[pos] != ']':
                wide_moves = self.compute_move(np - Coord(1, 0), None, direction)
                if len(wide_moves) == 0: return []

        changes = self.compute_move(np, pos, direction)
        if len(changes) == 0: return []
        changes.append(Move(pos, previous))
        changes += wide_moves
        return changes

def expand_line(line: AnyStr) -> AnyStr:
    return line.replace('O', '[]').replace('.', '..').replace('#', '##').replace('@', '@.')

if __name__ == '__main__':
    l = [x.strip() for x in open('p15.txt').readlines()]
    b = l.index('')
    puzzle = Puzzle(l[:b])
    wide_puzzle = Puzzle([expand_line(x) for x in l[:b]])


    for line in l[b+1:]:
        for c in line:
            puzzle.move(Direction.from_char(c))
            wide_puzzle.move(Direction.from_char(c))

    puzzle.print_map()
    print(f'The scores are {puzzle.score()} and {wide_puzzle.score()}')