#! /usr/bin/env python3

from multiprocessing import Pool

# Load the grid and initialize variables
def load_grid(file_path):
    with open(file_path, 'r', encoding='ascii') as file:
        data = file.read().rstrip()

    grid_str = data.splitlines()
    grid = [[1 if c == '#' else 0 for c in line] for line in grid_str if line]
    height, width = len(grid), len(grid[0])

    start_idx = data.strip().replace('\n', '').find('^')
    start_pos = (start_idx % width, start_idx // width)

    return grid, height, width, start_pos

# (dx, dy) [UP, RIGHT, DOWN, LEFT]
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# traverse the grid and return visited positions
def traverse_grid(start_pos, start_dir_idx, grid, width, height):
    pos = start_pos
    dir_idx = start_dir_idx
    visited = set([pos])

    while True:
        dx, dy = DIRS[dir_idx]
        nx, ny = (pos[0] + dx, pos[1] + dy)

        # bounds check
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            break

        if grid[ny][nx] == 1:
            dir_idx = (dir_idx + 1) % len(DIRS) # turn right
        else:
            pos = (nx, ny)

        visited.add(pos)

    return visited

# check if adding an obstacle creates a loop
def forms_loop(start_pos, start_dir_idx, extra_candidate, grid, width, height):
    unique_steps = set()
    pos = start_pos
    dir_idx = start_dir_idx

    while True:
        dx, dy = DIRS[dir_idx]
        nx, ny = (pos[0] + dx, pos[1] + dy)

        # bounds check
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            break

        if (nx, ny) == extra_candidate or grid[ny][nx] == 1:
            dir_idx = (dir_idx + 1) % len(DIRS) # turn right
        else:
            pos = (nx, ny)

        if (pos, dir_idx) in unique_steps:
            return True # cycle was formed!

        unique_steps.add((pos, dir_idx))

    return False

# Worker function to process a chunk of obstacle candidates
def process_candidates(chunk, start_pos, grid, width, height):
    local_loops = 0
    for cand in chunk:
        if forms_loop(start_pos, 0, cand, grid, width, height):
            local_loops += 1
    return local_loops

# Get number of loops formed by candidate obstacles, with parallelism
def determine_loops(obst_candidates, start_pos, grid, width, height, num_processes=16):
    candidates = list(obst_candidates)

    # split work between number of processes
    chunk_size = (len(candidates) + num_processes - 1) // num_processes
    chunks = [candidates[i:i + chunk_size] for i in range(0, len(candidates), chunk_size)]

    with Pool(num_processes) as pool:
        results = pool.starmap(process_candidates, [
            (chunk, start_pos, grid, width, height) for chunk in chunks
        ])

    return sum(results)

def main():
    grid, height, width, start_pos = load_grid('input.txt')

    # Part 1: Determine visited positions
    visited = traverse_grid(start_pos, 0, grid, width, height)

    print(len(visited)) # 5404

    # Part 2: Determine cycle-forming obstacle candidates
    obst_candidates = set(visited) # place obstacles along existing path

    # TODO: something clever to reduce seach space
    loops = determine_loops(obst_candidates, start_pos, grid, width, height)

    print(loops) # 1984

if __name__ == "__main__":
    main()
