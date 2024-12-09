from copy import deepcopy
from typing import Iterable, List, AnyStr, Sized


class Block(Sized):
    def __init__(self, capacity: int, data: List[int]):
        self.capacity = capacity
        self.data = data.copy()

    def free_space(self) -> int:
        return self.capacity - len(self.data)

    def insert_data(self, data: List[int]) -> None:
        if len(data) > self.free_space():
            raise Exception(f'File size {len(data)} exceeds free_space {self.free_space()}')
        self.data += data

    def pop(self, size: int) -> List[int]:
        if size > len(self.data):
            size = len(self.data)
        self.data, result = self.data[:-size], self.data[-size:]
        return result

    def checksum(self, first_subblock_id: int):
        result = 0
        for i in range(len(self.data)):
            result += self.data[i] * (i + first_subblock_id)
        return result

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f'Block({self.capacity}, {self.data})'

    def __str__(self) -> str:
        return ''.join([str(x) for x in self.data]) + '.' * self.free_space()


def generate_filesystem(line: AnyStr) -> List[Block]:
    """Parse test input.

    >>> generate_filesystem("12345")
    [Block(1, [0]), Block(2, []), Block(3, [1, 1, 1]), Block(4, []), Block(5, [2, 2, 2, 2, 2])]
    """
    blocks = []
    file_id = 0
    for i in range(len(line)):
        capacity = int(line[i])
        file_data = []
        if i % 2 == 0:
            file_data = [file_id] * capacity
            file_id += 1
        blocks.append(Block(capacity, file_data))
    return blocks


def compact_str(blocks: Iterable[Block]) -> str:
    """Helper for printf debugging

    >>> compact_str([Block(1, [0]), Block(2, []), Block(3, [1, 1, 1]), Block(4, []), Block(5, [2, 2, 2, 2, 2])])
    '0..111....22222'
    """
    return ''.join([str(x) for x in blocks])


def compact(blocks: List[Block]) -> List[Block]:
    """Compacts the file system.

    >>> compact_str(compact(generate_filesystem("12345")))
    '022111222......'
    >>> compact_str(compact(generate_filesystem("2333133121414131402")))
    '0099811188827773336446555566..............'
    """
    blocks = deepcopy(blocks)
    free_block = 1
    file_block = len(blocks) - 1
    if file_block % 2 == 1: file_block -= 1

    while free_block < file_block:
        available = blocks[free_block].free_space()
        if available == 0:
            free_block += 2
            continue

        data_to_insert = blocks[file_block].pop(available)
        blocks[free_block].insert_data(data_to_insert)

        if len(blocks[file_block]) == 0:
            file_block -= 2

    return blocks


def defrag(blocks: List[Block]) -> List[Block]:
    blocks = deepcopy(blocks)
    file_id = len(blocks) - 1
    if file_id % 2 == 1: file_id -= 1

    for file_id in range(file_id, 1, -2):
        file_size = len(blocks[file_id])
        for space_id in range(1, file_id, 2):
            if blocks[space_id].free_space() >= file_size:
                data_to_insert = blocks[file_id].pop(file_size)
                blocks[space_id].insert_data(data_to_insert)
                break
        file_id -= 2

    return blocks


def checksum(blocks: Iterable[Block]) -> int:
    """Calculate checksum of blocks.
    >>> checksum(compact(generate_filesystem("2333133121414131402")))
    1928
    """
    result = 0
    idx = 0
    for block in blocks:
        result += block.checksum(idx)
        idx += block.capacity

    return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    with open('p9.txt', 'r') as file:
        data = file.read().strip()

    blocks = generate_filesystem(data)
    compacted = compact(blocks)
    defragged = defrag(blocks)
    checksum_compacted = checksum(compacted)
    checksum_defraged = checksum(defragged)
    print(f'The checksums are {checksum_compacted} and {checksum_defraged}')
