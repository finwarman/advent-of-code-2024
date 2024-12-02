#! /usr/bin/env python3

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from util import get_input_data
from collections import defaultdict

# ==== INPUT ====

data = get_input_data()

rows = [row.split() for row in data.split('\n')[:-1] if row]
rows = [(int(l), int(r)) for l, r in rows]

# ==== SOLUTION ====

# part 1:

left, right = list(zip(*rows))
left, right = sorted(left), sorted(right)

total = 0
for i in range(len(rows)):
    total += abs(left[i] - right[i])

print("part 1:", total) # 2430334

# part 2:

r_counts = defaultdict(int)

for l, r in rows:
    r_counts[r] += 1

total = 0
for l, _ in rows:
    if l in r_counts:
        total += (l * r_counts[l])

print("part 2:", total) # 28786472
