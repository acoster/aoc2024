from collections.abc import Iterator
from typing import List, AnyStr


def find_all(haystack: AnyStr, needle: AnyStr) -> Iterator[int]:
    start = haystack.find(needle)
    while start >= 0:
        yield start
        start = haystack.find(needle, start + len(needle))


def count_horizontal(line: AnyStr, needle : AnyStr = 'XMAS') -> int:
    return len([x for x in find_all(line, needle)]) + len(
        [x for x in find_all(line, needle[::-1])])


def count_xmases(lines: List[AnyStr]) -> int:
    """Counts instances of the word XMAS in the puzzle.

    >>> count_xmases(['XMAS', 'SAMX', 'LEVI', 'YANV'])
    2
    >>> count_xmases(['XXXS', 'MNNA' , 'AAAM', 'SSSX'])
    2
    >>> count_xmases(['XaaX', '.MM.', '.AA.', 'S..S'])
    2
    >>> count_xmases(['MMMSXXMASM', 'MSAMXMSMSA', 'AMXSXMAAMM', 'MSAMASMSMX', 'XMASAMXAMM', 'XXAMMXXAMA', 'SMSMSASXSS', 'SAXAMASAAA', 'MAMMMXMMMM', 'MXMXAXMASX'])
    18
    """
    xmases = 0
    width = len(lines[0])

    for i in range(len(lines)):
        xmases += count_horizontal(lines[i])

        # Starting from the left, down and up diagonals
        xmases += count_horizontal(''.join([lines[i + k][k] for k in range(
            width - i)]))
        xmases += count_horizontal(
            ''.join([lines[i - k][k] for k in range(i + 1)]))

        if i == 0 or i == width - 1: continue

        # Starting from the right, down and up diagonals
        xmases += count_horizontal(''.join([lines[i + x][width - x - 1] for x in range(width - i)]))
        xmases += count_horizontal(''.join([lines[i - x][width - x - 1] for x
                                            in range(i + 1)]))


    for i in range(width):
        column = ''.join([x[i] for x in lines])
        xmases += count_horizontal(column)


    return xmases

def count_mas_exes(lines: List[AnyStr]) -> int:
    """Count exes made out of MAS.

    >>> count_mas_exes(['M.S', '.A.', 'M.S'])
    1
    >>> count_mas_exes(['MMMSXXMASM', 'MSAMXMSMSA', 'AMXSXMAAMM', 'MSAMASMSMX', 'XMASAMXAMM', 'XXAMMXXAMA', 'SMSMSASXSS', 'SAXAMASAAA', 'MAMMMXMMMM', 'MXMXAXMASX'])
    9
    """
    xmases = 0
    width = len(lines[0])

    for i in range(1, width - 1):
        for j in find_all(lines[i], 'A'):
            if j == 0 or j == width - 1: continue

            down = ''.join(
                [lines[i - 1][j - 1], lines[i][j], lines[i + 1][j + 1]])
            up = ''.join(
                [lines[i + 1][j - 1], lines[i][j], lines[i + -1][j + 1]])

            if count_horizontal(down, 'MAS') == 1 and count_horizontal(up, 'MAS') == 1:
                xmases += 1

    return xmases


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('p4.txt') as f:
        puzzle = f.read().splitlines()

    result = count_xmases(puzzle)
    print(f'XMAS count: {result}')

    result = count_mas_exes(puzzle)
    print(f'MAS exes count: {result}')