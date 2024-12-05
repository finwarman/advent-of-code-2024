#! /usr/bin/env python3

with open('input.txt', 'r') as file:
    input = file.read().rstrip()

# input='''
# 47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# '''

ordering_in, pages_in = [segment.splitlines() for segment in input.strip().split('\n\n')]

# if both X and Y are to be produced, X must be printed at some point before Y
ordering = []
for line in ordering_in:
    x, y = line.split('|')
    ordering.append( (int(x), int(y)) )

# page numbers of each update
page_lists = []
for line in pages_in:
    page_lists.append([int(x) for x in line.split(',')])

# print(ordering, page_lists)

# part 1: which updates are already in the right order

# build mappings
above_map = {} # x|y - y must be after x
below_map = {} # y|x - x must be after y
for o in ordering:
    x, y = o
    if x not in above_map:
        above_map[x] = set()
    if y not in below_map:
        below_map[y] = set()

    above_map[x].add(y)
    below_map[y].add(x)

valid_rows_middles = []

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
        valid_rows_middles.append(
            pages[len(pages)//2]
        )

# print(valid_rows_middles)
print(sum(valid_rows_middles)) # 4281
print()


# part 2


incorrect_updates = []

for pages in page_lists:
    valid = True
    # print(pages)
    for i, p in enumerate(pages):
        if p in above_map:
            if len(set(pages[i+1:]) - above_map[p]):
                valid = False
        if p in below_map:
            if len(set(pages[:i]) - below_map[p]):
                valid = False

    if not valid:
        incorrect_updates.append(pages)

sorted_page_middles = []

for pages in incorrect_updates:
    sorted_pages = sorted(
        pages,
        key=lambda x: (
            sum(1 for y in above_map.get(x, []) if y in pages) -
            sum(1 for y in below_map.get(x, []) if y in pages)
        )
    )
    sorted_page_middles.append(
        sorted_pages[len(sorted_pages)//2]
    )

# print(sorted_page_middles)
print(sum(sorted_page_middles)) # 5466
print()
