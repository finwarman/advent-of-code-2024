#! /usr/bin/env python3

import heapq


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

def main():
    maze = ''
    with open('input.txt', 'r') as f:
        maze = [list(line.strip()) for line in f.readlines()]

    start, end = find_start_and_end(maze)
    min_cost = dijkstra(maze, start, 'E', end)
    print(f"part 1 (lowest possible score): {min_cost}")

if __name__ == "__main__":
    main()
    # part 1: 85480
