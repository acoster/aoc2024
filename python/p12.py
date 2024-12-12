from aoc import Coord, Direction
from typing import List, AnyStr, Set

class Grid(object):
    def __init__(self, lines: List[AnyStr]):
        self._width = len(lines[0])
        self._height = len(lines)
        self.lines = lines

    def __getitem__(self, key: Coord):
        return self.lines[key.i][key.j]

    def in_bounds(self, key: Coord):
        return 0 <= key.i < self.height and 0 <= key.j < self.width

    def keys(self):
        for i in range (0, self._height):
            for j in range (0, self._width):
                yield Coord(i, j)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height



def flood_fill(grid: Grid):
    p1_answer = 0
    p2_answer = 0
    not_visited = {x for x in grid.keys()}

    while not_visited:
        start = not_visited.pop()
        letter = grid[start]

        stack = [start]
        edges = set()
        area, perimeter = 0, 0

        while stack:
            node = stack.pop()
            area += 1
            perimeter += 4
            for direction in Direction:
                new_node = node + direction.value
                if not grid.in_bounds(new_node): continue
                if grid[new_node] != letter:
                    edges.add((new_node, direction.value))
                    continue
                perimeter -= 1

                if new_node not in not_visited:
                    continue
                not_visited.remove(new_node)
                stack.append(new_node)

        p1_answer += area * perimeter

    return p1_answer, p2_answer


with open('p12.txt') as f:
    grid = Grid([l.strip() for l in f.readlines()])

print(flood_fill(grid))