import re
from dataclasses import dataclass
from typing import List, AnyStr, Iterator

import z3

from aoc import batched, Coord


@dataclass
class Puzzle:
    a: Coord
    b: Coord
    prize: Coord


def puzzles(lines: List[AnyStr]) -> Iterator[Puzzle]:
    pattern = re.compile(r'[^0-9]+(\d+)[^0-9]+(\d+)')
    for v in batched(lines, 4):
        match_a = pattern.findall(v[0])
        match_b = pattern.findall(v[1])
        match_prize = pattern.findall(v[2])

        yield Puzzle(
            Coord(int(match_a[0][0]), int(match_a[0][1])),
            Coord(int(match_b[0][0]), int(match_b[0][1])),
            Coord(int(match_prize[0][0]), int(match_prize[0][1]))
        )


def solve(puzzle: Puzzle, extra: int = 0) -> int:
    s = z3.Solver()
    a, b = z3.Ints("a b")

    s.add(puzzle.a.i * a + puzzle.b.i * b == (puzzle.prize.i + extra))
    s.add(puzzle.a.j * a + puzzle.b.j * b == (puzzle.prize.j + extra))

    if s.check() == z3.sat:
        m = s.model()
        return 3 * m[a].as_long() + m[b].as_long()
    return 0


if __name__ == '__main__':
    with open('p13.txt') as f:
        lines = f.readlines()

    total = 0
    total_extra = 0
    for puzzle in puzzles(lines):
        total += solve(puzzle)
        total_extra += solve(puzzle, 10000000000000)

    print(f'The number of tokens needed is {total}')
    print(f'The number of tokens needed with extra is {total_extra}')
