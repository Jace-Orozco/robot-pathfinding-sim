import numpy as np
import matplotlib.pyplot as plt

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
        else:
            raise IndexError("Cell coordinates out of bounds.")

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            raise IndexError("Cell coordinates out of bounds.")

    def display(self):
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.show()