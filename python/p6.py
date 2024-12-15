from typing import List, AnyStr, Tuple, Optional, Set, Iterator

from aoc import Coord, Direction


class Map(object):
    def __init__(self, lines: List[AnyStr]):
        self.lines = lines
        self.height = len(lines)
        self.width = len(self.lines[0])

        # Starting positions
        self.start = None

        for i in range(len(lines)):
            j = lines[i].find('^')
            if j != -1:
                self.start = Coord(i, j)
                break
        else:
            raise Exception('No starting position found!')

    def is_obstacle(self, p: Coord) -> bool:
        return p.in_bounds(self.lines) and self.lines[p.x][p.y] == '#'

    def walk(self, direction: Direction, start: Coord,
             extra_obstacle: Optional[Coord] = None) -> Iterator[Tuple[
        Coord, Direction]]:
        pos = start

        while True:
            yield pos, direction
            np = pos + direction.value
            if not np.in_bounds(self.lines):
                return

            while self.is_obstacle(np) or (
                    extra_obstacle is not None and np == extra_obstacle):
                direction = direction.turn_right()
                np = pos + direction.value

            pos = np

    def get_path(self) -> Set[Coord]:
        return {x[0] for x in self.walk(Direction.UP, self.start)}

    def is_loop(self, obstacle: Coord) -> bool:
        states = set()
        for pos, direction in self.walk(Direction.UP, self.start, obstacle):
            if (pos, direction) in states:
                return True
            states.add((pos, direction))
        return False


if __name__ == '__main__':
    puzzle = Map([x.strip() for x in open('p6.txt').readlines()])
    path = puzzle.get_path()
    print(f'Positions visited: {len(path)}')

    loops = 0
    for potential_obstacle in path:
        if puzzle.is_loop(potential_obstacle):
            loops += 1
    print(f'Loops: {loops}')
