import numpy as np
from collections import deque
from gridnav.grid import Grid, WALL, FREE
from gridnav.map_loader import MapData

def generate_map(width, height, wall_density = 0.25, seed = None, max_attempts = 100):
    rng = np.random.default_rng(seed)

    for attempt in range(max_attempts):
        grid = Grid(width, height)
        grid.grid[:, :] = (rng.random((height, width)) < wall_density).astype(int)

        grid.grid[0, :] = WALL # top row
        grid.grid[-1, :] = WALL # bottom row
        grid.grid[:, 0] = WALL # left column
        grid.grid[:, -1] = WALL # right column

        free_cells = np.argwhere(grid.grid == FREE)

        if len(free_cells) < 2:
            continue

        #workarount to keep [y, x] format for free_cells to match the grid's indexing
        i, j = rng.choice(len(free_cells), size=2, replace=False)
        start_cell = (int(free_cells[i][1]), int(free_cells[i][0]))  # (x, y)
        goal_cell = (int(free_cells[j][1]), int(free_cells[j][0]))  # (x, y)

        if is_reachable(grid, start_cell, goal_cell):
            return MapData(grid, start_cell, goal_cell)

    raise ValueError(f"Failed to generate a valid map after {max_attempts}")

def is_reachable(grid, start, goal):
    frontier = deque([start])
    seen = {start}
    while frontier:
        current = frontier.popleft()
        if current == goal:
            return True
        for neighbor in grid.neighbors(*current):
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return False

def save_map(map_data, path):
    grid = map_data.grid
    with open(path, "w") as f:
        for y in range(grid.height):
            line = ""
            for x in range(grid.width):
                if (x, y) == map_data.start:
                    line += "S"
                elif (x, y) == map_data.goal:
                    line += "G"
                elif grid.get_cell(x, y) == WALL:
                    line += "#"
                else:
                    line += "."
            f.write(line + "\n")