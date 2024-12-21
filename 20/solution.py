#! /usr/bin/env python3

import heapq
from collections import deque

with open('input.txt', 'r') as f:
    FILE = f.read()

# FILE = '''
# ###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############
# '''

START = -1, -1
END   = -1, -1

WALKABLE_CELLS = set()

TRACK = [list(row) for row in FILE.strip().splitlines()]
WIDTH, HEIGHT = len(TRACK[0]), len(TRACK)
for y in range(HEIGHT):
    for x in range(WIDTH):
        char = TRACK[y][x]
        if char == 'S':
            START = x, y
        elif char == 'E':
            END = x, y

        if char == '#':
            TRACK[y][x] = 1
        else:
            TRACK[y][x] = 0
            WALKABLE_CELLS.add((x, y))

def in_bounds(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

def get_neighbors(x, y, cheat=False):
    """
    return ([(nx, ny), cost], ...) for valid adjacent moves from (x, y).
    if cheat=True, walls are ignored.
    """
    moves = []
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny):
            # if cheat, ignore walls
            if cheat or TRACK[ny][nx] == 0:
                moves.append((nx, ny))
    return moves

def bfs_distances_to_end(end):
    """
    return dist[y][x] = minimal steps from (x, y) to 'end'
    for all cells that are walkable (TRACK[y][x] == 0).
    """
    ex, ey = end
    dist = [[float('inf')] * WIDTH for _ in range(HEIGHT)]
    dist[ey][ex] = 0

    queue = deque([(ex, ey)])

    while queue:
        x, y = queue.popleft()
        base_cost = dist[y][x]

        for (nx, ny) in get_neighbors(x, y, cheat=False):
            # if not a wall and we can improve the distance
            if dist[ny][nx] > base_cost + 1:
                dist[ny][nx] = base_cost + 1
                queue.append((nx, ny))

    return dist


def get_neighbors_no_wall(x, y):
    """return all normal (non-wall) neighbors of (x, y)."""
    moves = []
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and TRACK[ny][nx] == 0:
            moves.append((nx, ny))
    return moves

def find_single_wall_skips(dist_start, dist_end, fastest_route):
    """
    for each walkable cell (cx, cy), check if we can skip exactly one wall cell
    to reach some neighbor (nx, ny) in 2 steps. If that yields a route
    cheaper than fastest_route, record it.
    """
    possible_cheats = []

    for cy in range(HEIGHT):
        for cx in range(WIDTH):
            if dist_start[cy][cx] == float('inf'):
                continue  # not reachable from START in normal route
            if dist_end[cy][cx] == float('inf'):
                continue  # cannot eventually reach END in normal route
            # cost so far to (cx, cy)
            costC = dist_start[cy][cx]

            # explore all 'wall cells' adjacent to (cx, cy).
            # then from that wall cell, see what open neighbor you can reach.
            directions = [(0,1),(0,-1),(1,0),(-1,0)]
            for dx, dy in directions:
                wx, wy = cx+dx, cy+dy
                # check that (wx, wy) is valid wall
                if 0 <= wx < WIDTH and 0 <= wy < HEIGHT and TRACK[wy][wx] == 1:
                    # from this wall (wx, wy), check the other side
                    # if there's exactly one open neighbor beyond it:
                    #   => (nx, ny) such that (nx, ny) is also in-bounds and TRACK[ny][nx] == 0
                    #   => total cost for that skip is costC + 2 + dist_end[ny][nx]
                    for dx2, dy2 in directions:
                        nx, ny = wx+dx2, wy+dy2
                        if (nx, ny) != (cx, cy) and 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                            if TRACK[ny][nx] == 0:
                                # skip one wall cell (wx, wy) to get from (cx, cy) => (nx, ny)
                                # in exactly 2 moves.
                                total_cost = costC + 2 + dist_end[ny][nx]

                                if total_cost < fastest_route:
                                    time_saved = fastest_route - total_cost
                                    possible_cheats.append({
                                        "start_cell": (cx, cy),
                                        "wall_cell":  (wx, wy),
                                        "end_cell":   (nx, ny),
                                        "total_cost": total_cost,
                                        "time_saved": time_saved
                                    })

    return possible_cheats

def main():
    # compute min 'legit' cost from each path position to end
    dist_end = bfs_distances_to_end(END)
    dist_start = bfs_distances_to_end(START)

    # fastest 'legit' route from start to end
    fastest_route = dist_end[START[1]][START[0]]
    print("fastest legit route:", fastest_route)

    # find any point that can be shortened by cheating once
    # then get any that, from start, have an overall shortest route
    # faster 'dist'

    # min_diff = 0
    min_diff = 99 # save 100
    skips = find_single_wall_skips(dist_start, dist_end, fastest_route - min_diff)
    total = len(skips)

    # # print like in problem definition
    # time_saved_skips = {}
    # for skip in skips:
    #     if skip['time_saved'] not in time_saved_skips:
    #         time_saved_skips[skip['time_saved']] = 0
    #     time_saved_skips[skip['time_saved']] += 1
    # print()
    # for i in range(fastest_route):
    #     if i not in time_saved_skips:
    #         continue
    #     if time_saved_skips[i] == 1:
    #         print(f"There is one cheat that save {i + min_diff} picoseconds.")
    #     else:
    #         print(f"There are {time_saved_skips[i]} cheats that save {i + min_diff} picoseconds.")

    print()
    print(total) # part 1: 1323

if __name__ == "__main__":
    main()
