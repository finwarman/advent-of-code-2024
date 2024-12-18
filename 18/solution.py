#! /usr/bin/env python3

import heapq

with open('input.txt', 'r') as f:
    FILE = f.read()

# FILE = '''
# 5,4
# 4,2
# 4,5
# 3,0
# 2,1
# 6,3
# 2,4
# 1,5
# 0,6
# 3,3
# 2,6
# 5,1
# 1,2
# 5,5
# 2,5
# 6,5
# 1,4
# 0,4
# 6,4
# 1,1
# 6,1
# 1,0
# 0,5
# 1,6
# 2,0
# '''

BYTES = [(int(x.split(',')[0]), int(x.split(',')[1])) for x in FILE.strip().splitlines()]
POS = (0, 0)
# TARGET = (6, 6)
TARGET = (70, 70)

# BYTE_LIMIT = 12
BYTE_LIMIT = 1024

def get_neighbors(x, y, byte_set):
    moves = []
    directions = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    for (dx, dy) in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_y <= TARGET[1] and 0 <= new_x <= TARGET[0] \
           and (new_x, new_y) not in byte_set:
            moves.append(((new_x, new_y), 1))

    return moves

def dijkstra(start, end, byte_set):
    start_state = (0, start[0], start[1], 0)  # (cost, x, y, time)
    pq = []
    heapq.heappush(pq, start_state)
    visited = set()

    while pq:
        cost, x, y, time = heapq.heappop(pq)

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (x, y) == end:
            return cost

        for (new_x, new_y), move_cost in get_neighbors(x, y, byte_set):
            if (new_x, new_y) not in visited:
                heapq.heappush(pq, (cost + move_cost, new_x, new_y, time + 1))

    return float('inf')

print(dijkstra(POS, TARGET, set(BYTES[0:BYTE_LIMIT])))
# part 1: 370


# part 2: (brute force)

# todo: apply all bytes, remove until valid path to exit?

BLOCKING_BYTE = None
for i in range(BYTE_LIMIT, len(BYTES)):
    byte_set = set(BYTES[0:i])
    if dijkstra(POS, TARGET, byte_set) == float('inf'):
        BLOCKING_BYTE = BYTES[i-1]
        break

print(f"{BLOCKING_BYTE[0]},{BLOCKING_BYTE[1]}") # 65,6
