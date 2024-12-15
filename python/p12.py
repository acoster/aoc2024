from aoc import Coord, Direction
from typing import List, AnyStr, Iterator

class Grid(object):
    def __init__(self, lines: List[AnyStr]):
        self.__width = len(lines[0])
        self.__height = len(lines)
        self.__lines = lines

    def __getitem__(self, key: Coord):
        return self.__lines[key.x][key.y]

    def in_bounds(self, key: Coord) -> bool:
        return 0 <= key.y < self.height and 0 <= key.x < self.width

    def keys(self) -> Iterator[Coord]:
        for x in range (0, self.__width):
            for y in range (0, self.__height):
                yield Coord(x, y)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height



def solve(grid: Grid):
    p1_answer, p2_answer = 0, 0
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
                if not grid.in_bounds(new_node) or grid[new_node] != letter:
                    edges.add((node, direction))
                    continue
                perimeter -= 1

                if new_node not in not_visited:
                    continue

                not_visited.remove(new_node)
                stack.append(new_node)

        correction = 0
        for pos, direction in edges:
            left_neighbour = pos + direction.turn_left().value
            if (left_neighbour, direction) in edges:
                correction += 1

        p1_answer += area * perimeter
        p2_answer += area * (len(edges) - correction)

    return p1_answer, p2_answer


if __name__ == '__main__':
    with open('p12.txt') as f:
        grid = Grid([l.strip() for l in f.readlines()])

    print(solve(grid))