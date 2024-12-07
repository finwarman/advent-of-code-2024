#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().rstrip()

GRID_STR = DATA.splitlines()
GRID = [[1 if c == '#' else 0 for c in line] for line in GRID_STR if line]
HEIGHT, WIDTH = len(GRID), len(GRID[0])

START_IDX = DATA.strip().replace('\n', '').find('^')
START_POS = (START_IDX % WIDTH, START_IDX // WIDTH)

# (dx, dy) [UP, RIGHT, DOWN, LEFT]
DIRS = [( 0, -1), ( 1,  0),  ( 0,  1), (-1,  0)]

# part 1

POS = START_POS
DIR_IDX = 0 # up

VISITED = set()
VISITED.add(POS)

IN_BOUNDS = True
while IN_BOUNDS:
    dx, dy = DIRS[DIR_IDX]
    nx, ny = (POS[0] + dx, POS[1] + dy )

    # if obstacle or out of bounds
    if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
        break

    if GRID[ny][nx] == 1:
        DIR_IDX = (DIR_IDX + 1) % len(DIRS) # turn right
    else:
        POS = (nx, ny)
    VISITED.add(POS)

print(len(VISITED)) # 5404

# part 2

POS = START_POS
DIR_IDX = 0 # up

VISITED = set()
VISITED.add(POS)

UNIQUE_STEPS = set() # ((pos), (dir))
UNIQUE_STEPS.add((POS, DIR_IDX))

CORNERS = set()

IN_BOUNDS = True
while IN_BOUNDS:
    dx, dy = DIRS[DIR_IDX]
    nx, ny = (POS[0] + dx, POS[1] + dy )

    # if obstacle or out of bounds
    if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
        break

    if GRID[ny][nx] == 1:
        DIR_IDX = (DIR_IDX + 1) % len(DIRS) # turn right

        CORNERS.add((nx, ny))
    else:
        POS = (nx, ny)

    VISITED.add(POS)
    UNIQUE_STEPS.add((POS, DIR_IDX))


OBST_CANDIDATES = set([pos for pos in VISITED])

def forms_loop(start_pos, start_dir_idx, extra_candidate):
    pos = start_pos
    dir_idx = start_dir_idx

    unique_steps = set()

    in_bounds = True
    while in_bounds:
        dx, dy = DIRS[dir_idx]
        nx, ny = (pos[0] + dx, pos[1] + dy )

        # if obstacle or out of bounds
        if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
            break

        if (nx, ny) == extra_candidate or GRID[ny][nx] == 1:
            dir_idx = (dir_idx + 1) % len(DIRS) # turn right

            CORNERS.add((nx, ny))
        else:
            pos = (nx, ny)

        if (pos, dir_idx) in unique_steps:
            # a cycle!
            return True

        unique_steps.add((pos, dir_idx))

    return False


loops = 0
for cand in OBST_CANDIDATES:
    is_cycle = forms_loop(START_POS, 0, cand)
    if is_cycle:
        loops += 1

print(loops) # 1984

# TODO: something clever to reduce seach space
