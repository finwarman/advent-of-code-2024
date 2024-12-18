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

BYTE_SET = set(BYTES[0:BYTE_LIMIT])

def get_neighbors(x, y, time):
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
           and (new_x, new_y) not in BYTE_SET:
            moves.append(((new_x, new_y), 1))

    return moves

def dijkstra(start, end):
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

        for (new_x, new_y), move_cost in get_neighbors(x, y, time):
            if (new_x, new_y) not in visited:
                heapq.heappush(pq, (cost + move_cost, new_x, new_y, time + 1))

    return float('inf')

print(dijkstra(POS, TARGET)) # part 1: 370
