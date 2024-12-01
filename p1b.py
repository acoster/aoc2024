from collections import defaultdict

distribution_a = defaultdict(int)
distribution_b = defaultdict(int)

with open('inputs/input1.txt') as f:
    for line in f.readlines():
        a, b = line.split()
        distribution_a[int(a)] += 1
        distribution_b[int(b)] += 1

total_score = 0

for (n, count) in distribution_a.items():
    total_score += count * n * distribution_b[n]

print(f'Total score: {total_score}')