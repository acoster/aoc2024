from typing import List
import itertools

def op(value: int) -> List[int]:
    if value == 0:
        return [1]
    value_str = str(value)
    if len(value_str) % 2 == 0:
        mid = len(value_str) // 2
        return [int(value_str[:mid]), int(value_str[mid:])]

    return [2024 * value]

def solve(values: List[int], depth: int) -> int:
    """Performs an iteration,

    >>> solve([125, 17], 1)
    3
    >>> solve([125, 17], 25)
    55312
    """
    count = 0
    for v in values:
        step = [v]
        for i in range(depth):
            step = itertools.chain(*[op(x) for x in step])
        count += len(list(step))

    return count

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('p11.txt') as f:
        stones = [int(x) for x in f.read().strip().split(' ')]

    number_stones = solve(stones, 25)
    print(f'There are {number_stones} stones.')

