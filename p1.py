list_a = []
list_b = []

with open('input1.txt') as f:
    for line in f.readlines():
        a, b = line.split()
        list_a.append(int(a))
        list_b.append(int(b))

total_delta = 0

for a, b in zip(sorted(list_a), sorted(list_b)):
    total_delta += abs(a - b)

print(f'Total delta: {total_delta}')