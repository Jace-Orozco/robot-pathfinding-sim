from gridnav.planners import dijkstra, a_star, SQRT2
from gridnav.map_generator import generate_map
from gridnav.grid import Grid, WALL
import numpy as np
import pytest
import math

PLANNERS = [dijkstra, a_star]

def assert_valid_path(grid, path, start, goal):
    assert path[0] == start
    assert path[-1] == goal
    for a, b in zip(path, path[1:]):
        assert b in grid.neighbors(*a)   # every step must be a legal move

@pytest.mark.parametrize("seed", range(50))
def test_astar_matches_dijkstra(seed):
    m = generate_map(30, 20, wall_density=0.3, seed=seed)
    d = dijkstra(m.grid, m.start, m.goal)
    a = a_star(m.grid, m.start, m.goal)
    assert a.cost == pytest.approx(d.cost)
    assert a.nodes_expanded <= d.nodes_expanded
    assert_valid_path(m.grid, a.path, m.start, m.goal)
    assert_valid_path(m.grid, d.path, m.start, m.goal)


@pytest.mark.parametrize("planner", PLANNERS)
@pytest.mark.parametrize(
    ("start", "goal", "expected"),
    [
        ((0, 0), (4, 0), 4),               # straight line
        ((0, 0), (4, 4), 4 * SQRT2),       # pure diagonal
        ((0, 0), (4, 2), 2 + 2 * SQRT2),   # mix of both
        ((1, 1), (1, 1), 0),               # already at the goal
    ],
)
def test_known_costs_on_empty_grid(planner, start, goal, expected):
    grid = Grid(5, 5)
    result = planner(grid, start, goal)
    assert result.cost == pytest.approx(expected)


@pytest.mark.parametrize("planner", PLANNERS)
def test_no_path_through_full_wall(planner):
    grid = Grid(5, 5)
    for y in range(5):
        grid.set_cell(2, y, WALL)
    result = planner(grid, (0, 0), (4, 0))
    assert result.path is None
    assert result.cost == math.inf