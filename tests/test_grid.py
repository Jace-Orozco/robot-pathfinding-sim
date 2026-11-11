import numpy as np
import matplotlib.pyplot as plt
import pytest
from gridnav.grid import Grid, WALL

def test_grid_initialization():
    grid = Grid(5, 5)
    assert grid.width == 5
    assert grid.height == 5
    assert np.array_equal(grid.grid, np.zeros((5, 5), dtype=int))

def test_set_cell():
    grid = Grid(5, 5)
    grid.set_cell(2, 3, 1)
    assert grid.get_cell(2, 3) == 1

def test_set_cell_out_of_bounds():
    grid = Grid(5, 5)
    with pytest.raises(IndexError):
        grid.set_cell(5, 5, 1)

def test_get_cell_out_of_bounds():
    grid = Grid(5, 5)
    with pytest.raises(IndexError):
        grid.get_cell(5, 5)

#pytest runs the following function with each parameters 
#for a total of 4 extra tests
@pytest.mark.parametrize(
    ("x", "y"),
    [(-1, 0), (0, -1), (5, 0), (0, 3)],
)

def test_set_cell_invalid_coordinates(x, y):
    grid = Grid(5, 3)
    with pytest.raises(IndexError):
        grid.set_cell(x, y, 1)

#following five tests are for neighbor checking in said location and scenario
def test_neighbors_bottom_right_corner():
    grid = Grid(3, 3)
    assert sorted(grid.neighbors(2, 2)) == [(1, 1), (1, 2), (2, 1)]

def test_neighbors_top_left_corner():
    grid = Grid(3, 3)
    assert sorted(grid.neighbors(0, 0)) == [(0, 1), (1, 0), (1, 1)]

def test_neighbors_with_walls():
    grid = Grid(3, 3)
    grid.set_cell(1, 0, WALL)
    grid.set_cell(0, 1, WALL)
    assert sorted(grid.neighbors(0, 0)) == []

def test_neighbors_with_diagonal_wall():
    grid = Grid(3, 3)
    grid.set_cell(1, 0, WALL)
    grid.set_cell(0, 1, WALL)
    assert sorted(grid.neighbors(1, 1)) == [(1, 2), (2, 1), (2, 2)]
