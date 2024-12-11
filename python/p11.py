from typing import List
from functools import cache

@cache
def op(value: int) -> List[int]:
    if value == 0:
        return [1]
    value_str = str(value)
    if len(value_str) % 2 == 0:
        mid = len(value_str) // 2
        return [int(value_str[:mid]), int(value_str[mid:])]
    return [2024 * value]

@cache
def solve(v: int, depth: int):
    if depth == 0: return 1
    return sum([solve(x, depth - 1) for x in op(v)])


if __name__ == "__main__":
    with open('p11.txt') as f:
        stones = [int(x) for x in f.read().strip().split(' ')]

    number_stones_25 = sum([solve(x, 25) for x in stones])
    number_stones_75 = sum([solve(x, 75) for x in stones])
    print(f'There are {number_stones_25} and {number_stones_75} stone')

