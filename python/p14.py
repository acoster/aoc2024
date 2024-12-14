from dataclasses import dataclass
from typing import AnyStr
from enum import Enum
from copy import deepcopy
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

def solve_part_1(robots: list[Robot]) -> int:
    robots = deepcopy(robots)
    frequency_table = defaultdict(int)
    for robot in robots:
        robot.move(100)
        frequency_table[g.get_quadrant(robot.position)] += 1

    score = 1
    if Quadrant.NONE in frequency_table:
        frequency_table.pop(Quadrant.NONE)
    for quadrant in frequency_table:
        score *= frequency_table[quadrant]

    return score

def print_map(positions):
    for y in range(103):
        for x in range(101):
            if Coord(x, y) in positions:
                print('#', end='')
            else:
                print(' ', end='')
        print()


def solve_part_2(robots: list[Robot], iteration_limit: int = 11_000):
    robots = deepcopy(robots)
    for i in range(1, iteration_limit):
        positions = defaultdict(int)
        has_duplicates = False
        for robot in robots:
            robot.move(1)
            positions[robot.position] += 1
            if positions[robot.position] > 1:
                has_duplicates = True

        if has_duplicates: continue
        print(f'Time elapsed: {i} seconds')
        print_map(positions.keys())


if __name__ == '__main__':
    g = Grid(width=101, height=103)
    with open('p14.txt') as f:
        robots = [Robot(l, g) for l in f.readlines()]

    score = solve_part_1(robots)
    print(f'The score is {score}')
    solve_part_2(robots)