from collections.abc import Iterator
from typing import List, AnyStr


def find_all(haystack: AnyStr, needle: AnyStr) -> Iterator[int]:
    start = haystack.find(needle)
    while start >= 0:
        yield start
        start = haystack.find(needle, start + len(needle))


def count_horizontal(line: AnyStr):
    return len([x for x in find_all(line, 'XMAS')]) + len(
        [x for x in find_all(line, 'SAMX')])


def count_xmases(lines: List[AnyStr]) -> int:
    """Counts instances of the word XMAS.

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


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('p4.txt') as f:
        puzzle = f.read().splitlines()

    result = count_xmases(puzzle)
    print(f'XMAS count: {result}')