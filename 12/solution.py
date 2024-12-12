#! /usr/bin/env python3

from shapely.geometry import Polygon
from shapely.ops import unary_union

with open('input.txt', 'r', encoding='ascii') as file:
    FILE = file.read().strip()

# # Example grid
# FILE = '''
# RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE
# '''
DATA = [list(line) for line in FILE.strip().splitlines()]

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
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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

def calculate_polygon_area_perimeter(region_cells):
    # convert cells to a shapely polygon
    # each cell is a square, so expand each cell into its four corners
    cell_polygons = []
    for x, y in region_cells:
        cell_polygons.append(Polygon([
            (x, y), (x+1, y), (x+1, y+1), (x, y+1)
        ]))
    # merge all cell polygons into one using unary_union
    full_region = unary_union(cell_polygons)
    return full_region.area, full_region.length

regions = get_regions(DATA)
total_price = 0

for region_cells, plant_type in regions:
    area, perimeter = calculate_polygon_area_perimeter(region_cells)
    total_price += area * perimeter


# using logic from https://github.com/finwarman/advent-of-code-2023/blob/main/18/01.py
# going to use pips / shoelace e.g.
# see https://github.com/finwarman/advent-of-code-2023/blob/main/18/02.py

# part 1
print("Total price:", (total_price)) # 1451030
