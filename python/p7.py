from typing import List, Optional


def coalesce(a: Optional[int], b: Optional[int]) -> Optional[int]:
    if a is not None:
        return a
    return b


def solve(target: int, operands: List[int], acc: Optional[int] = None) -> Optional[int]:
    """Solve part 1 of day 7.

    >>> solve(190, [10, 19])
    190
    >>> solve(3267, [81, 40, 27])
    3267
    >>> solve(83, [17, 5])
    """
    if acc is None:
        return solve(target, operands[1:], operands[0])

    if acc > target:
        return None

    if len(operands) == 1:
        if acc + operands[0] == target or acc * operands[0] == target:
            return target
        return None

    return coalesce(
        solve(target, operands[1:], operands[0] * acc),
        solve(target, operands[1:], operands[0] + acc),
    )

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    total = 0
    with open('p7.txt') as f:
        for line in f.readlines():
            line = line.strip()
            target, ops = line.split(':')
            target = int(target)
            ops = [int(x) for x in ops.strip().split(' ')]

            if solve(target, ops) is not None:
                total += target

    print(f'The total is {total}')
