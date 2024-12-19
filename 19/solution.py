#! /usr/bin/env python3

from functools import lru_cache

with open('input.txt', 'r') as f:
    FILE = f.read()

PARTS = FILE.strip().split('\n\n')

PATTERNS = set(PARTS[0].split(', '))
DESIGNS = PARTS[1].split('\n')

MAX_PAT_LEN = max(len(p) for p in PATTERNS)

def is_possible(design):
    # memoized recursive helper function
    @lru_cache(None)
    def helper(remaining_design):
        if len(remaining_design) == 0:
            return True

        for i in range(1, min(MAX_PAT_LEN + 1, len(remaining_design) + 1)):
            prefix = remaining_design[:i]
            suffix = remaining_design[i:]
            if prefix in PATTERNS and helper(suffix):
                return True
        return False

    return helper(design)

total = 0
for design in DESIGNS:
    possible = is_possible(design)
    if possible:
        total += 1

print(total) # part 1: 308
