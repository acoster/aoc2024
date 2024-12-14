from dataclasses import dataclass
from typing import AnyStr
from enum import Enum
from collections import defaultdict
import re

from aoc import Coord

class Quadrant(Enum):
    NW = 1
    NE = 2
    SE = 3
    SW = 4
    NONE = 5

@dataclass(frozen=True)
class Grid:
    width: int
    height: int

    def get_quadrant(self, coord: Coord) -> Quadrant:
        if coord.i < self.width // 2:
            if coord.j < self.height // 2:
                return Quadrant.NW
            elif coord.j > self.height // 2:
                return Quadrant.SW
        elif coord.i > self.width // 2:
            if coord.j < self.height // 2:
                return Quadrant.NE
            elif coord.j > self.height // 2:
                return Quadrant.SE
        return Quadrant.NONE

class Robot:
    def __init__(self, line: AnyStr, grid: Grid):
        data = re.findall(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)

        self.position = Coord(int(data[0][0]), int(data[0][1]))
        self.velocity = Coord(int(data[0][2]), int(data[0][3]))
        self.grid = grid

    def move(self, seconds: int) -> None:
        self.position = Coord(
            (self.position.i + self.velocity.i * seconds) % self.grid.width,
            (self.position.j + self.velocity.j * seconds) % self.grid.height
        )

    def __repr__(self) -> str:
        return f'Robot({self.position}, {self.velocity})'


if __name__ == '__main__':
    g = Grid(width=101, height=103)
    with open('p14.txt') as f:
        robots = [Robot(l, g) for l in f.readlines()]

    frequency_table = defaultdict(int)
    for robot in robots:
        robot.move(100)
        frequency_table[g.get_quadrant(robot.position)] += 1

    score = 1
    for quadrant in frequency_table:
        if quadrant == Quadrant.NONE: continue
        score *= frequency_table[quadrant]

    print(f'The score is {score}')