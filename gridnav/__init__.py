import numpy as np
import matplotlib.pyplot as plt
from gridnav.grid import Grid
from gridnav.map_loader import load_map

def main():
    m = load_map("maps/simple.txt")
    m.display()

if __name__ == "__main__":
    main()
