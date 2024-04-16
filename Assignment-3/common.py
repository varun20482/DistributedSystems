MAPPERS=3
REDUCERS=3

ITERATIONS=10

input_path = "data/input/points.txt"
input_centroids_path = "data/input/centroids.txt"
mapper_ports = [f"[::]:{50000 + i}" for i in range(MAPPERS)]  
master_to_mapper_ports = [f"localhost:{50000 + i}" for i in range(MAPPERS)]
reducer_ports = [f"[::]:{51000 + i}" for i in range(REDUCERS)]
master_to_reducer_ports = [f"localhost:{51000 + i}" for i in range(REDUCERS)]

faulty_mappers = True
faulty_reducers = True

import random

def randomly_true():
    return random.random() < 0.5

if __name__ == '__main__':
    print("Mapper Ports:", mapper_ports)
    print("Reducer Ports:", reducer_ports)
    print(master_to_mapper_ports)
    print(master_to_reducer_ports)
