from typing import List, Optional


def coalesce(a: List[Optional[int]]) -> Optional[int]:
    for x in a:
        if x is not None:
            return x


def int_cat(a: int, b: int) -> int:
    return int('%d%d' % (a, b))


def solve(target: int, operands: List[int], acc: Optional[int] = None, enable_concatenation: bool = False) -> Optional[
    int]:
    """Solve part 1 of day 7.

    >>> solve(190, [10, 19])
    190
    >>> solve(3267, [81, 40, 27])
    3267
    >>> solve(83, [17, 5])
    >>> solve(156, [15, 6], enable_concatenation=True)
    156
    """
    if acc is None:
        return solve(target, operands[1:], operands[0], enable_concatenation)

    if acc > target:
        return None

    if len(operands) == 1:
        if acc + operands[0] == target or acc * operands[0] == target:
            return target
        if enable_concatenation:
            if int_cat(acc, operands[0]) == target:
                return target
        return None

    next_ops = [
        solve(target, operands[1:], operands[0] * acc, enable_concatenation),
        solve(target, operands[1:], operands[0] + acc, enable_concatenation)
    ]

    if enable_concatenation:
        next_ops.append(solve(target, operands[1:], int_cat(acc, operands[0]), enable_concatenation))

    return coalesce(next_ops)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    total = 0
    total_with_concatenation = 0
    with open('p7.txt') as f:
        for line in f.readlines():
            line = line.strip()
            target, ops = line.split(':')
            target = int(target)
            ops = [int(x) for x in ops.strip().split(' ')]

            if solve(target, ops) is not None:
                total += target

            if solve(target, ops, enable_concatenation=True) is not None:
                total_with_concatenation += target

    print(f'The total is {total}')
    print(f'The total with concatenation is {total_with_concatenation}')
