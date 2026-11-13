import csv
import pandas as pd
from pathlib import Path
from gridnav.map_generator import generate_map
from gridnav.planners import dijkstra, a_star

DENSITIES = [0.1, 0.2, 0.3, 0.35]
SEEDS = range(100)
WIDTH, HEIGHT = 60, 40
PLANNERS = {"dijkstra": dijkstra, "a_star": a_star}

def run_benchmark():
    rows = []
    for density in DENSITIES:
        for seed in SEEDS:
            m = generate_map(WIDTH, HEIGHT, wall_density=density, seed=seed)
            for name, planner in PLANNERS.items():
                result = planner(m.grid, m.start, m.goal)
                rows.append({
                    "density": density,
                    "seed": seed,
                    "planner": name,
                    "cost": result.cost,
                    "nodes_expanded": result.nodes_expanded,
                    "runtime_ms": result.runtime * 1000,
                    "path_length": len(result.path) if result.path else 0,
                })
    return rows

def save_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def summarize(csv_path):
    df = pd.read_csv(csv_path)
    summary = df.groupby(["density", "planner"])[["nodes_expanded", "runtime_ms", "cost"]].mean()
    print(summary.round(2))

    nodes = summary["nodes_expanded"].unstack()        # one column per planner
    speedup = nodes["dijkstra"] / nodes["a_star"]
    print("\nA* node reduction (Dijkstra / A*):")
    print(speedup.round(2))

def main():
    rows = run_benchmark()
    save_csv(rows, "results/benchmark.csv")
    summarize("results/benchmark.csv")

if __name__ == "__main__":
    main()
