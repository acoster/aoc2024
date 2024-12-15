from typing import Iterator, List, Optional, Set, Tuple

from aoc import Coord, Direction


class Grid(object):
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def trailheads(self) -> Iterator[Coord]:
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    yield Coord(x, y)

    def visit(self, pos: Coord, path: List[Coord],
              peaks: Optional[Set[Coord]] = None) -> int:
        if self.grid[pos.y][pos.x] == 9:
            if peaks is not None:
                peaks.add(pos)
            return 1

        altitude = self.grid[pos.y][pos.x]

        score = 0
        for direction in Direction:
            np = pos + direction.value
            if np in path or not np.in_bounds(self.grid):
                continue
            na = self.grid[np.y][np.x]
            if na - altitude == 1:
                score += self.visit(np, path + [pos], peaks)

        return score

    def solve(self) -> Tuple[int, int]:
        p1_result = 0
        p2_result = 0
        for trailhead in self.trailheads():
            peaks = set()
            p2_result += self.visit(trailhead, [], peaks)
            p1_result += len(peaks)
        return p1_result, p2_result


if __name__ == '__main__':

    with open('p10.txt', 'r') as f:
        grid = []
        for line in f.readlines():
            line = line.strip()
            grid.append([x for x in map(int, line)])

    grid = Grid(grid)
    scores, ratings = grid.solve()

    print(f'Total score is {scores}, total ratings is {ratings}')
