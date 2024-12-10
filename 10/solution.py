#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

DATA = [list(map(int, list(line))) for line in FILE.strip().splitlines()]

WIDTH = len(DATA) # square

TRAILHEADS = [(x, y) for y in range(WIDTH)
                     for x in range(WIDTH) if DATA[y][x] == 0]

ADJ = [(-1, 0), (1, 0), (0, -1), (0, 1)] # (dx, dy)
def get_valid_neighbours(pos):
    x, y = pos
    value = DATA[y][x]

    neighbours = []
    for dx, dy in ADJ:
        nx, ny = dx+x, dy+y
        if 0 <= nx < WIDTH and 0 <= ny < WIDTH \
            and DATA[ny][nx] == value+1:
                neighbours.append((nx, ny))
    return neighbours

def get_trailhead_score(start_pos):
    q = [start_pos]
    trail_ends = set() # unique trail ends
    paths = 0 # distinct paths
    while q:
        x, y = pos = q.pop(0)
        value = DATA[y][x]
        if value == 9:
            paths += 1
            trail_ends.add((x, y))
            continue
        ns = get_valid_neighbours(pos)
        for n in ns:
            q.append(n)
    return len(trail_ends), paths # part 1, part 2

# part 1, part 2
total_1, total_2 = 0, 0
for trailhead in TRAILHEADS:
    score_1, score_2 = get_trailhead_score(trailhead)
    total_1 += score_1
    total_2 += score_2

print(total_1) # 667
print(total_2) # 1344
