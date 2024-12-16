#! /usr/bin/env python3

import heapq
from collections import defaultdict

def find_start_and_end(maze):
    start, end = None, None
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
    return start, end

def get_neighbors(x, y, direction, maze):
    moves = []
    directions = [
        ((0, -1), 'N'),
        ((1, 0), 'E'),
        ((0, 1), 'S'),
        ((-1, 0), 'W')
    ]

    current_idx = [d[1] for d in directions].index(direction)

    # turning actions
    for i, (_, new_dir) in enumerate(directions):
        if i != current_idx:
            turn_cost = 1000
            moves.append(((x, y, new_dir), turn_cost))

    # moving actions
    for (dx, dy), new_dir in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] != '#':
            move_cost = 1
            if new_dir == direction:
                moves.append(((new_x, new_y, new_dir), move_cost))

    return moves

def dijkstra(maze, start, start_dir, end):
    start_state = (0, start[0], start[1], start_dir)  # (cost, x, y, direction)

    pq = []

    heapq.heappush(pq, start_state)

    visited = set()

    while pq:
        cost, x, y, direction = heapq.heappop(pq)

        if (x, y, direction) in visited:
            continue

        visited.add((x, y, direction))

        if (x, y) == end:
            return cost

        for (new_x, new_y, new_dir), move_cost in get_neighbors(x, y, direction, maze):
            if (new_x, new_y, new_dir) not in visited:
                heapq.heappush(pq, (cost + move_cost, new_x, new_y, new_dir))

    return float('inf')


# def heuristic(x, y, end):
#     return abs(x - end[0]) + abs(y - end[1])
# manhattan distance towards correct location

def dijkstra_all_paths(maze, start, start_dir, end, optimal_cost):
    start_state = (0, start[0], start[1], start_dir)  # (cost, x, y, direction)

    pq = []
    heapq.heappush(pq, start_state)

    visited = defaultdict(lambda: float('inf'))  # track the minimum cost for each state
    paths = defaultdict(list)  # track all paths leading to a state

    visited[(start[0], start[1], start_dir)] = 0
    paths[(start[0], start[1], start_dir)].append([(start[0], start[1])])

    while pq:
        cost, x, y, direction = heapq.heappop(pq)

        # if this state has already been visited with a lower cost, skip it
        if cost > visited[(x, y, direction)]:
            continue

        # dont exceed known best cost
        if cost > optimal_cost:
            continue

        for (new_x, new_y, new_dir), move_cost in get_neighbors(x, y, direction, maze):
            new_cost = cost + move_cost

            # we found a cheaper or equivalent cost path to a state
            if new_cost <= visited[(new_x, new_y, new_dir)]:
                if new_cost < visited[(new_x, new_y, new_dir)]:
                    visited[(new_x, new_y, new_dir)] = new_cost
                    paths[(new_x, new_y, new_dir)] = []  # reset paths for this state if new cost is better

                # append new paths
                for path in paths[(x, y, direction)]:
                    new_path = path + [(new_x, new_y)]
                    if new_path not in paths[(new_x, new_y, new_dir)]:
                        paths[(new_x, new_y, new_dir)].append(new_path)

                heapq.heappush(pq, (new_cost, new_x, new_y, new_dir))

    # extract all paths with minimum cost to the end position
    shortest_paths = []
    min_cost = float('inf')

    for (state_x, state_y, state_dir), cost in visited.items():
        if (state_x, state_y) == end and cost <= min_cost:
            min_cost = cost
            shortest_paths.extend(paths[(state_x, state_y, state_dir)])

    return min_cost, shortest_paths


def main():
    maze = ''
    with open('input.txt', 'r') as f:
        maze = [list(line.strip()) for line in f.readlines()]

    start, end = find_start_and_end(maze)
    min_cost = dijkstra(maze, start, 'E', end)
    print(f"part 1 (lowest possible score): {min_cost}")


    start, end = find_start_and_end(maze)
    min_cost, all_shortest_paths = dijkstra_all_paths(maze, start, 'E', end, min_cost)

    # VERY SLOW!
    print(f"part 1 (lowest possible score): {min_cost}")
    print(f"part 2 (all tiles on shortest paths):")
    unique_tiles = set(tile for path in all_shortest_paths for tile in path)
    print(len(unique_tiles))

if __name__ == "__main__":
    main()
    # part 1: 85480
    # part 2: 518
