from gridnav.grid import Grid, WALL, FREE
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt

Position = tuple[int, int] #(x, y) coordinates

@dataclass
class MapData:
    grid: Grid
    start: Position
    goal: Position

    def display(self):
            plt.imshow(self.grid.grid, cmap='binary', interpolation='nearest', vmin = 0, vmax = 1)
            sx, sy = self.start
            gx, gy = self.goal
            plt.plot(sx, sy, 'go', label='Start')  # Start position in green
            plt.plot(gx, gy, 'r*', label='Goal')   # Goal position in red
            plt.legend()
            plt.show()

def load_map(path):
    with open(path) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    if not lines:
        raise ValueError("The map file is empty.")

    height, width = len(lines), len(lines[0])
    grid = Grid(width, height)
    start = goal = None

    for y, line in enumerate(lines):
        if len(line) != width:
            raise ValueError(f"Line {y} in the map file does not match the expected width of {width}.")
        for x, char in enumerate(line):
            if char == '#':
                grid.set_cell(x, y, WALL)
            elif char in '.SG':
                grid.set_cell(x, y, FREE)
                if char == 'S':
                    if start is not None:
                        raise ValueError("Multiple start positions found in the map file.")
                    start = (x, y)
                elif char == 'G':
                    if goal is not None:
                        raise ValueError("Multiple goal positions found in the map file.")
                    goal = (x, y)
            else:
                raise ValueError(f"Invalid character '{char}' in the map file at position ({x}, {y}).")

    if start is None or goal is None:
        raise ValueError("The map file must contain exactly one start position 'S' and one goal position 'G'.")
    

    return MapData(grid=grid, start=start, goal=goal)

