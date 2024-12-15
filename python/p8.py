from collections import defaultdict
from itertools import permutations
from typing import List, AnyStr, Set, Tuple

from aoc import Coord


class Solution(object):
    def __init__(self, roof_map: List[AnyStr]):
        self.h = len(roof_map)
        self.w = len(roof_map[0])
        self.roof_map = roof_map
        self.antennas = defaultdict(list)

        for y in range(len(roof_map)):
            for x in range(len(roof_map[y])):
                if roof_map[y][x] != '.':
                    self.antennas[roof_map[y][x]].append(Coord(x, y))

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
    p1_antinodes, p2_antinodes = s.find_anti_nodes()
    print(f'p1 Antinodes: {len(p1_antinodes)}')
    print(f'p2 Antinodes: {len(p2_antinodes)}')
