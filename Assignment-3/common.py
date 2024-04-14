MAPPERS=2
REDUCERS=2
CENTROIDS=10

ITERATIONS=10

coordinates_from=-10
coordinates_to=10

input_path = "input/points.txt"
mapper_ports = [f"[::]:{50000 + i}" for i in range(MAPPERS)]  
master_to_mapper_ports = [f"localhost:{50000 + i}" for i in range(MAPPERS)]
reducer_ports = [f"[::]:{51000 + i}" for i in range(REDUCERS)]
master_to_reducer_ports = [f"localhost:{51000 + i}" for i in range(REDUCERS)]

if __name__ == '__main__':
    print("Mapper Ports:", mapper_ports)
    print("Reducer Ports:", reducer_ports)
    print(master_to_mapper_ports)
    print(master_to_reducer_ports)
