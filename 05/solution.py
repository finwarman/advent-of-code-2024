#! /usr/bin/env python3

with open('input.txt', 'r') as file:
    input = file.read().rstrip()

inp_a, inp_b = [segment.splitlines() for segment in input.strip().split('\n\n')]

ordering   = [tuple(map(int, line.split('|'))) for line in inp_a]
page_lists = [list(map(int, line.split(','))) for line in inp_b]

# build mappings
above_map = {} # x|y, y must be after x
below_map = {} # y|x, x must be after y
for o in ordering:
    x, y = o
    if x not in above_map:
        above_map[x] = set()
    if y not in below_map:
        below_map[y] = set()

    above_map[x].add(y)
    below_map[y].add(x)

# part 1

middle_sum = 0

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

print(middle_sum) # 4281

# part 2

sorted_middle_sum = 0

for pages in page_lists:
    valid = True
    for i, p in enumerate(pages):
        if p in above_map:
            if len(set(pages[i+1:]) - above_map[p]):
                valid = False
        if p in below_map:
            if len(set(pages[:i]) - below_map[p]):
                valid = False

    if not valid:
        sorted_pages = sorted(
            pages,
            key=lambda x: (
                sum(1 for y in above_map.get(x, []) if y in pages) -
                sum(1 for y in below_map.get(x, []) if y in pages)
            )
        )
        sorted_middle_sum += sorted_pages[len(sorted_pages)//2]

print(sorted_middle_sum) # 5466
