import numpy as np
import matplotlib.pyplot as plt

WALL, FREE = 1, 0

DIRECTIONS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1)
]

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def set_cell(self, x, y, value):
        if self.in_bounds(x, y):
            self.grid[y][x] = value
        else:
            raise IndexError("Cell coordinates out of bounds.")

    def get_cell(self, x, y):
        if self.in_bounds(x, y):
            return self.grid[y][x]
        else:
            raise IndexError("Cell coordinates out of bounds.")

    def neighbors(self, x, y):
        result = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if not self.in_bounds(nx, ny) or self.get_cell(nx, ny) == WALL:
                continue
            if dx != 0 and dy != 0:
                if self.grid[y][nx] == WALL or self.grid[ny][x] == WALL:
                    continue
            if self.in_bounds(nx, ny) and self.get_cell(nx, ny) == FREE:
                result.append((nx, ny))
        return result

    def display(self):
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.show()