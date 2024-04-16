import random

def generate_coordinates(num_points, min_val, max_val):
    with open("points.txt", "w") as f:
        for _ in range(num_points):
            x = random.uniform(min_val, max_val)
            y = random.uniform(min_val, max_val)
            f.write(f"{x} {y}\n")

def generate_centroids(num_points, min_val, max_val):
    with open("centroids.txt", "w") as f:
        for _ in range(num_points):
            x = random.uniform(min_val, max_val)
            y = random.uniform(min_val, max_val)
            f.write(f"{x}, {y}\n")


num_data_points=20
coordinates_from=-10
coordinates_to=10
num_centroids=3
generate_coordinates(num_data_points, coordinates_from, coordinates_to)
generate_centroids(num_centroids, coordinates_from, coordinates_to)
