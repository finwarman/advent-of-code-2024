#! /usr/bin/env python3

with open('input.txt', 'r') as file:
    input = file.read().rstrip()

# input = '''
# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........
# '''

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

    # Keep current direction
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

seen = set()
q = [pos for pos in x_pos]
# q = [pos for pos in x_pos[0:1]]
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

# X-MAS

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

x_mas_count = 0

valid_strs = set([
    'SSMM',
    'MSMS',
    'SMSM',
    'MMSS',
])

for a in a_pos:
    x, y, char = a

    invalid = False
    ns = []
    for (dx, dy) in ADJ:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
            invalid = True
            break
        new_char = grid[ny][nx]
        if new_char in ('M', 'S'):
            ns.append((nx, ny, new_char))
    if invalid:
        continue

    # two mas in shape of an x

    c_s, c_m = 0, 0
    str = ''
    for n in ns:
        _, _, char = n
        if char == 'S':
            c_s += 1
        elif char == 'M':
            c_m += 1

        str += (char)

    if str in valid_strs:
        x_mas_count += 1

print(x_mas_count) # 1737
