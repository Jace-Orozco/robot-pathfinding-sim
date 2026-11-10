import numpy as np
import matplotlib.pyplot as plt
from gridnav.grid import Grid

def main():
    # Create a grid of size 10x10
    grid = Grid(10, 10)

    # Set some cells to different values
    grid.set_cell(2, 3, 1)
    grid.set_cell(5, 5, 1)
    grid.set_cell(7, 8, 1)

    # Display the grid
    grid.display()

if __name__ == "__main__":
    main()