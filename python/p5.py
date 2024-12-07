import graphlib
from collections import defaultdict
from typing import Mapping, List


class Solver(object):
    def __init__(self, dependencies: Mapping[int, List[int]]):
        self.__dependencies = dependencies

    def find_middle_page(self, pages: List[int], fix_mistakes: bool = False) -> int:
        """Finds the middle page, or return 0 if invalid input was provided."""

        sorter = graphlib.TopologicalSorter()
        for page, predecessors in self.__dependencies.items():
            if page not in pages: continue
            sorter.add(page, *[p for p in predecessors if p in pages])

        visited_pages = []
        has_fixed = False

        sorter.prepare()
        ready_pages = set(sorter.get_ready())
        for page in pages:
            if len(ready_pages) == 0:
                ready_pages = set(sorter.get_ready())
                if len(ready_pages) == 0:
                    return 0

            if page not in ready_pages:
                if not fix_mistakes:
                    return 0

                has_fixed = True
                if len(ready_pages) != 1:
                    raise Exception('Too many to choose from')

                page = ready_pages.pop()
                ready_pages.add(page)

            visited_pages.append(page)
            ready_pages.remove(page)
            sorter.done(page)

        if not has_fixed and fix_mistakes:
            return 0

        return visited_pages[int((len(pages) - 1) / 2)]


sum_without_fix = 0
sum_with_fixed = 0

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
            sum_with_fixed += solver.find_middle_page(p, fix_mistakes=True)
            sum_without_fix += solver.find_middle_page(p, fix_mistakes=False)

print(f'Result without fixes: {sum_without_fix}')
print(f'Result with fixes: {sum_with_fixed}')
