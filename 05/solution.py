#! /usr/bin/env python3

with open('input.txt', 'r') as file:
    input = file.read().rstrip()

inp_a, inp_b = [segment.splitlines() for segment in input.strip().split('\n\n')]

ordering   = [tuple(map(int, line.split('|'))) for line in inp_a]
page_lists = [list(map(int, line.split(','))) for line in inp_b]

# build mappings
above_map = {} # x|y, y must be after x
below_map = {} # y|x, x must be after y
for x, y in ordering:
    above_map.setdefault(x, set()).add(y)
    below_map.setdefault(y, set()).add(x)

# part 1

middle_sum = 0
invalid_pages = []

for pages in page_lists:
    valid = True
    for i, p in enumerate(pages):
        if p in above_map:
            if len(set(pages[i+1:]) - above_map[p]):
                valid = False
        if p in below_map:
            if len(set(pages[:i]) - below_map[p]):
                valid = False

    if valid:
        middle_sum += pages[len(pages)//2]
    else:
        invalid_pages.append(pages) # for part 2

print(middle_sum) # 4281

# part 2

sorted_middle_sum = 0

for pages in invalid_pages:
    sorted_pages = sorted(
        pages,
        key=lambda x: (
            sum(1 for y in above_map.get(x, []) if y in pages) -
            sum(1 for y in below_map.get(x, []) if y in pages)
        )
    )
    sorted_middle_sum += sorted_pages[len(sorted_pages)//2]

print(sorted_middle_sum) # 5466


## alternate (faster) solution,
ordering = set(tuple(map(int, line.split('|'))) for line in inp_a)
updates = [list(map(int, line.split(','))) for line in inp_b]

# assumes an ordering entry exists for every page pair
def validate_update(update, ordering):
    return all(
        (update[i], update[j]) in ordering
        for i in range(len(update)) for j in range(i + 1, len(update))
    )

def part_a(ordering, updates):
    valid_updates = filter(lambda up: validate_update(up, ordering), updates)
    return sum(update[len(update) // 2] for update in valid_updates)

def part_b(ordering, updates):
    invalid_updates = filter(lambda up: not validate_update(up, ordering), updates)
    sorted_middle_sum = 0
    for update in invalid_updates:
        sorted_update = sorted(update, key=lambda x: 
            # compare 'above' and 'below' from ordering:
            sum(1 for y in update if (x, y) in ordering) -
            sum(1 for y in update if (y, x) in ordering)
        )
        sorted_middle_sum += sorted_update[len(sorted_update) // 2]
    return sorted_middle_sum

print()
print("Part A:", part_a(ordering, updates))
print("Part B:", part_b(ordering, updates))
