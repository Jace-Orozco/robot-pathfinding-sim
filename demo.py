from gridnav.map_generator import generate_map
from gridnav.planners import a_star

m = generate_map(60, 40, wall_density = 0.25, seed = 85)
result = a_star(m.grid, m.start, m.goal)
print(f"cost={result.cost:.2f}  nodes expanded={result.nodes_expanded}")
m.display(path=result.path, save_to="docs/astar_example.png")
