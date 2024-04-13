import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
import common

def generate_coordinates(num_points, min_val, max_val):
    with open("points.txt", "w") as f:
        for _ in range(num_points):
            x = random.uniform(min_val, max_val)
            y = random.uniform(min_val, max_val)
            f.write(f"({x:.2f},{y:.2f})\n")

generate_coordinates(10, common.coordinates_from, common.coordinates_to)
