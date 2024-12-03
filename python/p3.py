from typing import AnyStr, List, Tuple
import re


def run(data: AnyStr, enable_do: bool = False) -> int:
    """Find all valid multiplications, do them and return their sum.

    >>> run('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))')
    161
    >>> run("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))", True)
    48
    """
    total = 0
    pattern = re.compile(r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))")
    enabled = True
    for match in  pattern.findall(data):
        if match[0].startswith("mul"):
            total += int(match[1]) * int(match[2]) if enabled else 0
        elif enable_do:
            enabled = match[0] == 'do()'

    return total

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('p3.txt') as f:
        d = f.read()
        result = run(d, False)
        print(f'The result is {result}')
        result = run(d, True)
        print(f'The result with do is {result}')
