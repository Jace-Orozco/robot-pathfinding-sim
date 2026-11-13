import heapq, math, time
from dataclasses import dataclass 

SQRT2 = math.sqrt(2)

def step_cost(a, b):
    return SQRT2 if a[0] != b[0] and a[1] != b[1] else 1

#octile instead of euclidean or manhattan distance for heuristic
#euclidean explores more cells and manhattan incorrectly estimates diagonal movement cost
def octile(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return (dx + dy) + (SQRT2 - 2) * min(dx, dy)

def zero(a, b):
    return 0.0

def reconstruct(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

@dataclass
class PlanResult:
    path: list | None       #list of (x, y) from S to G, or None if no path found
    cost: float             #math.inf if there is no path
    nodes_expanded: int
    runtime: float          #seconds

def search(grid, start, goal, heuristic):
    t0 = time.perf_counter()
    open_heap = [(heuristic(start, goal), 0.0, start)]  # (f, g, position)
    g = {start: 0.0}
    came_from = {}
    closed = set()
    expanded = 0

    while open_heap:
        f, g_cur, current = heapq.heappop(open_heap)
        if current in closed:
            continue           #skip outdated entries in the priority queue
        closed.add(current)
        expanded += 1

        if current == goal:
            path = reconstruct(came_from, current)
            return PlanResult(path, g_cur, expanded, time.perf_counter() - t0)

        for neighbor in grid.neighbors(*current):
            new_g = g_cur + step_cost(current, neighbor)
            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f, new_g, neighbor))
                came_from[neighbor] = current

    return PlanResult(None, math.inf, expanded, time.perf_counter() - t0)

def dijkstra(grid, start, goal):
    return search(grid, start, goal, zero)

def a_star(grid, start, goal):
    return search(grid, start, goal, octile)