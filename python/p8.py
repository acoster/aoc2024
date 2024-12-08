from collections import defaultdict
from itertools import permutations
from typing import List, AnyStr, Set, Tuple


class Coord(object):
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j

    def in_bounds(self, grid: List[AnyStr]) -> bool:
        return 0 <= self.i < len(grid) and 0 <= self.j < len(grid[0])

    def __add__(self, other):
        return Coord(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Coord(self.i - other.i, self.j - other.j)

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))

    def __repr__(self):
        return f"Coord({self.i}, {self.j})"


class Solution(object):
    def __init__(self, roof_map: List[AnyStr]):
        self.h = len(roof_map)
        self.w = len(roof_map[0])
        self.roof_map = roof_map
        self.antennas = defaultdict(list)

        for i in range(len(roof_map)):
            for j in range(len(roof_map[i])):
                if roof_map[i][j] != '.':
                    self.antennas[roof_map[i][j]].append(Coord(i, j))

    def find_anti_nodes(self) -> Tuple[Set[Coord], Set[Coord]]:
        p1_anti_nodes = set()
        p2_anti_nodes = set()

        for frequency in self.antennas:
            for a1, a2 in permutations(self.antennas[frequency], 2):
                delta = a2 - a1
                antinode = a2 + delta
                p2_anti_nodes.add(a2)
                if antinode.in_bounds(self.roof_map):
                    p1_anti_nodes.add(antinode)
                    while antinode.in_bounds(self.roof_map):
                        p2_anti_nodes.add(antinode)
                        antinode += delta

        return p1_anti_nodes, p2_anti_nodes


if __name__ == '__main__':
    with open('p8.txt') as f:
        l = [x.strip() for x in f.readlines()]

    s = Solution(l)
    (p1_antinodes, p2_antinodes) = s.find_anti_nodes()
    print(f'p1 Antinodes: {len(p1_antinodes)}')
    print(f'p2 Antinodes: {len(p2_antinodes)}')
