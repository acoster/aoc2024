import graphlib
from typing import Mapping, List, AnyStr
from collections import defaultdict


class Solver(object):
    def __init__(self, dependencies: Mapping[int, List[int]]):
        self.__dependencies = dependencies

    def find_middle_page(self, pages:  List[int]) -> int:
        """Finds the middle page, or return 0 if invalid input was provided."""

        sorter = graphlib.TopologicalSorter()
        for page, predecessors in self.__dependencies.items():
            if page not in pages: continue
            sorter.add(page, *[p for p in predecessors if p in pages])

        sorter.prepare()
        ready_pages = set(sorter.get_ready())
        for page in pages:
            if len(ready_pages) == 0:
                ready_pages = set(sorter.get_ready())
                if len(ready_pages) == 0:
                    return 0

            if page not in ready_pages:
                return 0
            ready_pages.remove(page)
            sorter.done(page)

        return pages[int((len(pages) -1) / 2)]




s = 0
dependencies = defaultdict(list)
with open('p5.txt') as f:
    for line in f.readlines():
        line = line.strip()

        if line.find('|') != -1:
            a, b = line.split('|')
            dependencies[int(b)].append(int(a))
        elif len(line) == 0:
            solver = Solver(dependencies)
        elif line.find(',') != -1:
            p = [int(x) for x in line.split(',')]
            s += solver.find_middle_page(p)

print(s)