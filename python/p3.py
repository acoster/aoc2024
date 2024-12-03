from typing import AnyStr, List, Tuple
import re


def run(data: AnyStr) -> int:
    """Find all valid multiplications, do them and return their sum.

    >>> run('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))')
    161
    """
    total = 0
    pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    for a, b in  pattern.findall(data):
        total += int(a) * int(b)
    return total

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('p3.txt') as f:
        result = run(f.read())
        print(f'The result is {result}')