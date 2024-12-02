from typing import AnyStr, Sequence


def is_safe(row: list[int], dampen = False) -> bool:
    """Determine if a string is safe or not.

    >>> is_safe([7, 6, 4, 2, 1])
    True
    >>> is_safe([8, 6, 4, 4, 1], dampen = True)
    True
    >>> is_safe([1, 3, 6, 7, 9], dampen = False)
    True
    >>> is_safe([1, 3, 2, 4, 5], dampen = True)
    True
    """

    signal = 1 if row[0] < row[1] else -1

    for i in range(1, len(row)):
        delta = (row[i] - row[i - 1]) * signal
        if delta < 1 or delta > 3:
            if dampen:
                # Test the 3 possible sequences
                seq1 = row[:i] + row[i + 1:]
                seq2 = row[:i - 1] + row[i:]
                seq3 = row[:i - 2] + row[i - 1:]
                return is_safe(seq1, False) or is_safe(seq2, False) or is_safe(seq3, False)
            else:
                return False

    return True

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    safe = 0
    safe_with_dampening = 0

    with open('inputs/p2.txt', 'r') as file:
        for line in file.readlines():
            values = [int(x) for x in  line.split()]
            if is_safe(values, False):
                safe += 1
                safe_with_dampening += 1
            elif is_safe(values, True):
                safe_with_dampening += 1
    print(f'Safe: {safe}, Safe with dampening: {safe_with_dampening}')
