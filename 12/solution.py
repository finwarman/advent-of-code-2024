#! /usr/bin/env python3

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

DATA = [list(line) for line in FILE.strip().splitlines()]

# LEFT, DOWN, RIGHT, UP
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def get_regions(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def bfs(x, y):
        queue = [(x, y)]
        visited[x][y] = True
        plant_type = grid[x][y]
        region_cells = []

        while queue:
            cx, cy = queue.pop(0)
            region_cells.append((cx, cy))
            for dx, dy in DIRS:
                nx, ny = cx + dx, cy + dy
                if is_valid(nx, ny) and not visited[nx][ny] and grid[nx][ny] == plant_type:
                    visited[nx][ny] = True
                    queue.append((nx, ny))
        return region_cells, plant_type

    regions = []
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                cells, plant_type = bfs(i, j)
                regions.append((cells, plant_type))
    return regions


def part_1_cost(grid, regions):
    total_cost = 0

    for region in regions:
        cells, label = region
        perimeter = 0

        for x, y in cells:
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                # if neighbor is out of bounds or a different type
                if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])) or grid[nx][ny] != label:
                    perimeter += 1

        area = len(cells)
        total_cost += area * perimeter

    return total_cost

def part_2_cost(grid, regions):
    total_cost = 0

    # get perimeter cells, grouped by (up, down, left, right)
    def get_direction_sets(region_cells, label):
        direction_sets = {d: set() for d in DIRS}
        for x, y in region_cells:
            for _, (dx, dy) in enumerate(DIRS):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])) or grid[nx][ny] != label:
                    direction_sets[(dx, dy)].add((x, y))
        return direction_sets

    def count_sides(direction_set):
        sides = 0

        def dfs(cell):
            stack = [cell]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) not in direction_set:
                    continue
                direction_set.remove((cx, cy)) # mark as 'visited'
                for dx, dy in DIRS:
                    neighbor = (cx + dx, cy + dy)
                    if neighbor in direction_set:
                        stack.append(neighbor)

        while direction_set:
            sides += 1
            peeked_cell = next(iter(direction_set)) # arbitrary start point
            dfs(peeked_cell)

        return sides

    for region in regions:
        region_cells, label = region
        area = len(region_cells)

        direction_sets = get_direction_sets(region_cells, label)

        # count sides for all four directions
        total_sides = sum(
            count_sides(direction_set) for direction_set in direction_sets.values()
        )

        total_cost += area * total_sides

    return total_cost


regions = get_regions(DATA)

print(part_1_cost(DATA, regions)) # 1451030
print(part_2_cost(DATA, regions)) # 859494
