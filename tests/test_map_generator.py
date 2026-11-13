from gridnav.map_generator import is_reachable
from map_generator import generate_map, save_map

def test_generate_map():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert map_data.grid.shape == (10, 10)
    assert map_data.start != map_data.goal
    assert is_reachable(map_data.grid, map_data.start, map_data.goal)


def test_same_map_generation_with_same_seed():
    map_data1 = generate_map(10, 10, wall_density=0.2, seed=42)
    map_data2 = generate_map(10, 10, wall_density=0.2, seed=42)
    assert np.array_equal(map_data1.grid, map_data2.grid)
    assert map_data1.start == map_data2.start
    assert map_data1.goal == map_data2.goal

def test_border_walls():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert np.all(map_data.grid[0, :] == 1)  # Top row
    assert np.all(map_data.grid[-1, :] == 1)  # Bottom row
    assert np.all(map_data.grid[:, 0] == 1)  # Left column
    assert np.all(map_data.grid[:, -1] == 1)  # Right column

def test_different_start_goal_positions():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert map_data.start != map_data.goal

def test_is_reachable_function():
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    assert is_reachable(map_data.grid, map_data.start, map_data.goal)

def test_density_zero():
    map_data = generate_map(10, 10, wall_density=0.0, seed=42)
    assert np.all(map_data.grid[1:-1, 1:-1] == 0)  # All inner cells should be free

def test_density_too_high():
    with pytest.raises(ValueError):
        generate_map(10, 10, wall_density=1.0, seed=42)  # Should raise an error due to no free cells

def test_save_map(tmp_path):
    map_data = generate_map(10, 10, wall_density=0.2, seed=42)
    file_name = "test_map"
    save_map(map_data, tmp_path, file_name)
    saved_file = tmp_path / f"{file_name}.npz"
    assert saved_file.exists()
    loaded_data = np.load(saved_file)
    assert np.array_equal(loaded_data['grid'], map_data.grid)
    assert tuple(loaded_data['start']) == map_data.start
    assert tuple(loaded_data['goal']) == map_data.goal