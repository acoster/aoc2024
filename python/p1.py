from collections import defaultdict

list_a = []
list_b = []

distribution_a = defaultdict(int)
distribution_b = defaultdict(int)

with open('p1.txt') as f:
    for line in f.readlines():
        a, b = line.split()
        a, b = int(a), int(b)
        list_a.append(a)
        list_b.append(b)

        distribution_a[a] += 1
        distribution_b[b] += 1

total_delta = 0
for a, b in zip(sorted(list_a), sorted(list_b)):
    total_delta += abs(a - b)
print(f'Total delta: {total_delta}')

total_score = 0
for n, count in distribution_a.items():
    total_score += count * n * distribution_b[n]

print(f'Total score: {total_score}')