#!/usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    DATA = file.read().strip()

# parse input
GRID = [[1 if c == '#' else 0 for c in line] for line in DATA.splitlines()]
HEIGHT, WIDTH = len(GRID), len(GRID[0])

player_str_idx = DATA.strip().replace('\n', '').find('^')
START_POS = (player_str_idx % WIDTH, player_str_idx // WIDTH)

# direction consts
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
(UP, RIGHT, DOWN, LEFT) = [0, 1, 2, 3] # indices

# simulate path, return positions in path
def traverse_path():
    pos, dir_idx = START_POS, UP

    visited = set([pos])
    while True:
        x, y = pos
        dx, dy = DIRS[dir_idx]
        nx, ny = x + dx, y + dy

        if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
            break # out of bounds

        if GRID[ny][nx] == 1:
            dir_idx = (dir_idx + 1) % len(DIRS) # turn right
        else:
            pos = (nx, ny) # move to next cell

        visited.add(pos)

    return visited


# build a jump table mapping each (x, y, dir) to (next_pos, new_direction)
# i.e. for each state in a path, get the next turning point due to an obstacle.
# this lets us skip simulating individual steps.
def build_jump_table():
    jump_table = {}

    # horizontal
    for y in range(HEIGHT):
        # LEFT->UP collision turns
        last_obstacle = (-1, y)
        for x in range(WIDTH):
            if GRID[y][x] == 1:
                last_obstacle = (x + 1, y)
            jump_table[(x, y, LEFT)] = (last_obstacle, UP)

        # RIGHT->DOWN collision turns
        last_obstacle = (WIDTH, y)
        for x in range(WIDTH - 1, -1, -1):
            if GRID[y][x] == 1:
                last_obstacle = (x - 1, y)
            jump_table[(x, y, RIGHT)] = (last_obstacle, DOWN)

    # vertical
    for x in range(WIDTH):
        # UP->RIGHT collision turns
        last_obstacle = (x, -1)
        for y in range(HEIGHT):
            if GRID[y][x] == 1:
                last_obstacle = (x, y + 1)
            jump_table[(x, y, UP)] = (last_obstacle, RIGHT)

        # DOWN->LEFT collision turns
        last_obstacle = (x, HEIGHT)
        for y in range(HEIGHT - 1, -1, -1):
            if GRID[y][x] == 1:
                last_obstacle = (x, y - 1)
            jump_table[(x, y, DOWN)] = (last_obstacle, LEFT)

    return jump_table

def simulate_with_obstacle(obstacle, jump_table):
    pos, dir_idx = START_POS, UP
    x_obs, y_obs = obstacle

    visited_states = set([(pos, dir_idx)])

    in_bounds = True
    while in_bounds:
        x, y = pos
        if x != x_obs and y != y_obs:
            # not on the same row or column as obstacle: use jump table
            jump_key = (x, y, dir_idx)
            if jump_key not in jump_table:
                return 0 # invalid jump, out-of-bounds (no cycle)
            pos_new, dir_new = jump_table[jump_key]
            pos, dir_idx = pos_new, dir_new
        else:
            # on the same row or column as obstacle: step-by-step
            dx, dy = DIRS[dir_idx]
            nx, ny = x + dx, y + dy

            if not(0 <= nx < WIDTH and 0 <= ny < HEIGHT):
                return 0 # next step is out-of-bounds (no cycle)

            # check collision, including candidate obstacle
            if (nx, ny) == obstacle or GRID[ny][nx] == 1:
                dir_idx = (dir_idx + 1) % len(DIRS) # turn right
            else:
                pos = (nx, ny) # move to next cell

        if (pos, dir_idx) in visited_states:
            return 1 # cycle detected!
        visited_states.add((pos, dir_idx))

        in_bounds = (0 <= x < WIDTH and 0 <= y < HEIGHT)

    return 0 # no cycle


if __name__ == "__main__":
    # part 1: get unique positions in traversal path
    path = traverse_path()
    print(len(path)) # 5404

    # part 2: detect cycles with added candidate obstacles
    obst_candidates = list(path) # each position in path
    jump_table = build_jump_table() # simulation shortcuts

    loops = sum(simulate_with_obstacle(obstacle, jump_table)
                for obstacle in obst_candidates)
    print(loops) # 1984
