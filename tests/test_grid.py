import numpy as np
import matplotlib.pyplot as plt
import pytest
from gridnav.grid import Grid

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