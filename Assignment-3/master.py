import common
import grpc
import kmeans_pb2
import kmeans_pb2_grpc
import random
import subprocess
import sys

def read_file_in_chunks(file_name, num_chunks, index):
    if(index < 0 or index >= num_chunks):
        print("Invalid MAPPER Index")
        return 
    
    with open(file_name, 'r') as f:
        lines = f.readlines()

    num_lines = len(lines)
    chunk_size = num_lines // num_chunks

    start_index = index * chunk_size
    end_index = start_index + chunk_size
    if( index == num_chunks - 1 ):
        end_index = num_lines

    print(f"Chunk {index + 1}: Start Index: {start_index}, End Index: {end_index}")

    chunk_lines = lines[start_index:end_index]

    for line in chunk_lines:
        print(line.strip())

    return kmeans_pb2.chunk(start_index = start_index, end_index = end_index)

def run():
    mapper_stubs = []
    reducer_stubs = []
    for i in range(0, common.MAPPERS):
        mapper_channel = grpc.insecure_channel(common.master_to_mapper_ports[i])
        mapper_stubs.append(kmeans_pb2_grpc.KMeansStub(mapper_channel))

    for i in range(0, common.REDUCERS):
        reducer_channel = grpc.insecure_channel(common.master_to_reducer_ports[i])
        reducer_stubs.append(kmeans_pb2_grpc.KMeansStub(reducer_channel))
    
    mapper_chunks = []
    for i in range(0, common.MAPPERS):
        mapper_chunks.append(read_file_in_chunks(common.input_path, common.MAPPERS, i))

    centroids = []
    print("============= INITIAL CENTROIDS =============")
    for i in range(0, common.CENTROIDS):
        x = random.uniform(common.coordinates_from, common.coordinates_to)
        y = random.uniform(common.coordinates_from, common.coordinates_to)
        centroids.append(kmeans_pb2.coordinate(x=x, y=y))
    for i, item in enumerate(centroids):
            print(f"({item.x:.2f},{item.y:.2f})", end="")
            if i < len(centroids) - 1:
                print(", ", end="")
            else:
                print()
    print("=============================================")

    for i in range(common.ITERATIONS):
        print(f"=================ITERATION:{i}=================")

        for i in range(0, common.MAPPERS):
            print(f"===================MAPPER_{i}==================")
            response = mapper_stubs[i].Map(kmeans_pb2.mapInfo(indices=mapper_chunks[i], centroids=centroids))
            if(response.success):
                print("MAP OPERATION SUCCESSFUL")
            else:
                print("MAP OPERATION FAILED")
            print("=============================================")
        
        updated_centroids = []
        for i in range(0, common.REDUCERS):
            print(f"==================REDUCER_{i}==================")
            response = reducer_stubs[i].Reduce(kmeans_pb2.reduceInfo(id = i))
            print("UPDATED CENTROIDS BY REDUCER:")
            for item in response.dict:
                print(f"{item.key}:({item.value.x},{item.value.y})\n")
            updated_centroids.append(response.dict)
            print("=============================================")

        prev_centroids = []
        for i in range(0, len(centroids)):
            prev_centroids.append(kmeans_pb2.coordinate(x=centroids[i].x, y=centroids[i].y))

        for reducer in updated_centroids:
            for item in reducer:
                centroids[item.key] = item.value
        
        print("============= UPDATED CENTROIDS =============")
        for i, item in enumerate(centroids):
            print(f"({item.x:.2f},{item.y:.2f})", end="")
            if i < len(centroids) - 1:
                print(", ", end="")
            else:
                print()
        print("=============================================")
 
        same = True
        for i in range(0, len(centroids)):
            if(centroids[i].x != prev_centroids[i].x or centroids[i].y != prev_centroids[i].y):
                same = False
        if(same):
            print(f"==================CONVERGED==================")
            print("=============================================")
            break
        else:
            print(f"================NOT CONVERGED================")

        print("=============================================")

if __name__ == '__main__':
    original_stdout = sys.stdout
    with open("dump/master.txt", 'w') as f:
        sys.stdout = f
        run()
        sys.stdout = original_stdout