#! /usr/bin/env python3

with open('input.txt', 'r') as file:
    input = file.read().rstrip()

grid = [list(line) for line in input.splitlines() if line]
WIDTH, HEIGHT = len(grid[0]), len(grid)

# part 1

# find all 'X' positions to start
x_pos = []
for x in range(WIDTH):
    for y in range(HEIGHT):
        if grid[y][x] == 'X':
            x_pos.append((x, y, 'X', None))

NEXT_CHAR = {'X': 'M', 'M': 'A', 'A': 'S'}
ADJ = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
]

def get_valid_neighbours(pos):
    x, y, char, dir = pos

    neighbours = []

    # preserve current direction
    if dir is None:
        adj = ADJ
    else:
        adj = [dir]

    for (dx, dy) in adj:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
            continue

        new_char = grid[ny][nx]
        if new_char == NEXT_CHAR[char]:
            neighbours.append((nx, ny, new_char, (dx, dy)))

    return neighbours

total_xmas = 0

q = [pos for pos in x_pos]
while len(q):
    pos = q.pop(0)
    neighbours = get_valid_neighbours(pos)
    for n in neighbours:
        _, _, char, _ = n
        if char == 'S':
            total_xmas += 1
        else:
            q.append(n)

print(total_xmas) # 2358

# part 2

# find all 'A' positions to start
a_pos = []
for x in range(WIDTH):
    for y in range(HEIGHT):
        if grid[y][x] == 'A':
            a_pos.append((x, y, 'A'))

# get 'X' shape around
ADJ = [
    (-1, -1), (1, -1),
    (-1,  1), (1,  1),
]
VALID_NEIGHBOUR_STRINGS = set([
    'SSMM',
    'MSMS',
    'SMSM',
    'MMSS',
])

x_mas_count = 0

for a in a_pos:
    x, y, char = a

    neighbour_str = ''
    for (dx, dy) in ADJ:
        nx, ny = x + dx, y + dy
        if not (nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT):
            new_char = grid[ny][nx]
            if new_char in ('M', 'S'):
                neighbour_str += new_char

    if len(neighbour_str) == 4 and \
       neighbour_str in VALID_NEIGHBOUR_STRINGS:
        x_mas_count += 1

print(x_mas_count) # 1737
