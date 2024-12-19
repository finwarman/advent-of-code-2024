#! /usr/bin/env python3

from functools import cache

with open('input.txt', 'r') as f:
    FILE = f.read()

PARTS = FILE.strip().split('\n\n')

PATTERNS = set(PARTS[0].split(', '))
DESIGNS = PARTS[1].split('\n')

MAX_PAT_LEN = max(len(p) for p in PATTERNS)

def get_arrangements(design):
    @cache
    def helper(remaining_design):
        if len(remaining_design) == 0:
            return 1 # base case (empty design)

        count = 0
        for i in range(1, min(MAX_PAT_LEN + 1, len(remaining_design) + 1)):
            prefix, suffix = remaining_design[:i], remaining_design[i:]
            if prefix in PATTERNS:
                count += helper(suffix) # sum of ways to arrange remaining design
        return count

    return helper(design)

total_possible, total_arrangements = 0, 0
for design in DESIGNS:
    arrangements = get_arrangements(design)
    total_possible += 1 if arrangements > 0 else 0
    total_arrangements += arrangements

print(total_possible) # part 1: 308
print(total_arrangements) # part 2: 662726441391898
