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


def walk(lines : List[AnyStr]) -> int:
    direction = Direction.UP
    i, j = 0, 0
    height = len(lines)
    width = len(lines[0])
    for x in range(len(lines)):
        y = lines[x].find('^')
        if y != -1:
            i = x
            j = y
            break
    else:
        raise Exception('No ^ found in map!')

    positions = 0
    while True:
        if lines[i][j] != 'X':
            positions += 1
        lines[i] = lines[i][:j] + 'X' + lines[i][j+1:]
        next_i, next_j = next_position(direction, i, j)
        if is_out_of_bounds(next_i, next_j, height, width):
            return positions

        if lines[next_i][next_j] == '#':
            direction = turn_right(direction)
        else:
            i, j = next_i, next_j


puzzle = [x.strip() for x in  open('p6.txt').readlines()]
result = walk(puzzle)
print(f'Positions visited: {result}')