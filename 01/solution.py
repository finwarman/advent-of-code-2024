#! /usr/bin/env python3

from collections import defaultdict

# ==== INPUT ====

INPUT = 'input.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

rows = [row.split() for row in data.split('\n')[:-1] if row]
rows = [(int(l), int(r)) for l, r in rows]

# ==== SOLUTION ====

# part 1:

left, right = list(zip(*rows))
left, right = sorted(left), sorted(right)

total = 0
for i in range(len(rows)):
    total += abs(left[i] - right[i])

print(total) # 2430334

# part 2:

r_counts = defaultdict(int)

for l, r in rows:
    r_counts[r] += 1

total = 0
for l, _ in rows:
    if l in r_counts:
        total += (l * r_counts[l])

print(total) # 28786472
