#! /usr/bin/env python3

from more_itertools import partition

with open('input.txt', 'r', encoding='ascii') as file:
    data = file.read().rstrip()

inp_a, inp_b = [segment.splitlines() for segment in data.strip().split('\n\n')]

ORDERING = set(tuple(map(int, line.split('|'))) for line in inp_a)
UPDATES = [list(map(int, line.split(','))) for line in inp_b]

def validate_update(update):
    """
    Validates the update by checking if for every page, there exists
    an ordering entry for every page above it, in the correct order.
    Assumes an ordering entry exists for every page pair.

    Returns True if the update is valid, False otherwise.
    """
    return all(
        (update[i], update[j]) in ORDERING
        for i in range(len(update))
        for j in range(i + 1, len(update))
    )

INVALID_UPDATES, VALID_UPDATES = partition(validate_update, UPDATES)

part_a = sum(update[len(update) // 2] for update in VALID_UPDATES)

def part_b():
    '''
    Sorts the invalid updates, using the sorting key:
    (number of pages x should come before) - (number of pages x should come after)
    This places pages that need to come before more pages, earlier.

    Returns the sum of the middle values of the newly sorted update arrays.
    '''
    sorted_middle_sum = 0
    for update in INVALID_UPDATES:
        sorted_update = sorted(update, key=lambda x, update=update:
            sum(1 for y in update if (x, y) in ORDERING) -
            sum(1 for y in update if (y, x) in ORDERING)
        )
        sorted_middle_sum += sorted_update[len(sorted_update) // 2]
    return sorted_middle_sum

print("Part A:", part_a)
print("Part B:", part_b())
