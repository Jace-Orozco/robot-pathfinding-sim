from gridnav.map_generator import generate_map, save_map, is_reachable
from gridnav.map_loader import load_map
import numpy as np
import pytest

def test_generate_map():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert map_data.grid.grid.shape == (10, 10)
    assert map_data.start != map_data.goal
    assert is_reachable(map_data.grid, map_data.start, map_data.goal)


def test_same_map_generation_with_same_seed():
    map_data1 = generate_map(10, 10, wall_density=0.2, seed=42)
    map_data2 = generate_map(10, 10, wall_density=0.2, seed=42)
    assert np.array_equal(map_data1.grid.grid, map_data2.grid.grid)
    assert map_data1.start == map_data2.start
    assert map_data1.goal == map_data2.goal

def test_border_walls():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert np.all(map_data.grid.grid[0, :] == 1)  # Top row
    assert np.all(map_data.grid.grid[-1, :] == 1)  # Bottom row
    assert np.all(map_data.grid.grid[:, 0] == 1)  # Left column
    assert np.all(map_data.grid.grid[:, -1] == 1)  # Right column

def test_different_start_goal_positions():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert map_data.start != map_data.goal

def test_is_reachable_function():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert is_reachable(map_data.grid, map_data.start, map_data.goal)

def test_density_zero():
    map_data = generate_map(10, 10, wall_density=0.0, seed=42)
    assert np.all(map_data.grid.grid[1:-1, 1:-1] == 0)  # All inner cells should be free

def test_density_too_high():
    with pytest.raises(ValueError):
        generate_map(10, 10, wall_density=1.0, seed=42)  # Should raise an error due to no free cells

def test_save_and_load_round_trip(tmp_path):
    original = generate_map(10, 10, wall_density=0.2, seed=42)
    path = tmp_path / "test_map.txt"
    save_map(original, path)
    loaded = load_map(path)
    assert np.array_equal(loaded.grid.grid, original.grid.grid)
    assert loaded.start == original.start
    assert loaded.goal == original.goal
