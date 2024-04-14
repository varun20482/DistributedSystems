import common
import grpc
import kmeans_pb2
import kmeans_pb2_grpc
import random
import subprocess
import sys
import uuid
import concurrent.futures

def read_entries(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            coordinates = []
            for line in lines:
                x, y = map(float, line.strip()[1:-1].split(','))
                coordinates.append(kmeans_pb2.coordinate(x = x, y = y))
            
            return coordinates
    except FileNotFoundError:
        print("File not found!")
    except IndexError:
        print("Invalid start_index or end_index.")
    except Exception as e:
        print("An error occurred:", str(e))

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

failed_mappers = []
mapper_stubs = []
reducer_stubs = []
mapper_chunks = []
master_id = ""

failed_reducers = []
updated_centroids = []

def map_chunk(i, centroids, itr):
    print(f"===================MAPPER_{i + 1}==================")
    try:
        
        response = mapper_stubs[i].Map(kmeans_pb2.mapInfo(indices=mapper_chunks[i], centroids=centroids, master_id=master_id, iteration=itr))
        if response.success:
            print(f"MAP OPERATION SUCCESSFUL: CHUNK {i + 1}")
        else:
            print(f"MAP OPERATION FAILED: RETURNED FAILED: CHUNK {i + 1}")
            failed_mappers.append(i)
    except grpc.RpcError as e:
        print(f"MAP OPERATION FAILED: RPC ERROR: CHUNK {i + 1}")
        failed_mappers.append(i)
    print("=============================================")

def retry_map_chunk(idx, centroids, itr):
    print(f"RETRYING FAILED MAP: CHUNK ID: {idx + 1}")
    idx_success = False
    while(not idx_success):
        for i in range(0, common.MAPPERS):
            try:
                response = mapper_stubs[i].Map(kmeans_pb2.mapInfo(indices=mapper_chunks[idx], centroids=centroids, master_id=master_id, iteration=itr))
                if response.success:
                    idx_success = True
                    print(f"MAP OPERATION SUCCESSFUL: CHUNK {idx + 1}: BY MAPPER {i + 1}")
                    break
                else:
                    print(f"MAP OPERATION FAILED: RETURNED FAILED: CHUNK {idx + 1}")
            except grpc.RpcError as e:
                print(f"MAP OPERATION FAILED: RPC ERROR: CHUNK {idx + 1}")

def reduce_operation(i, itr):
    print(f"==================REDUCER_{i + 1}==================")
    try:
        response = reducer_stubs[i].Reduce(kmeans_pb2.reduceInfo(id=i, iteration=itr))
        if response.success:
            print(f"REDUCE OPERATION SUCCESSFUL: REDUCE ID {i + 1}: BY REDUCER {i + 1}")
            print("UPDATED CENTROIDS BY REDUCER:")
            for item in response.dict:
                print(f"{item.key}:({item.value.x},{item.value.y})\n")
            updated_centroids.append(response.dict)
        else:
            print(f"REDUCE OPERATION FAILED: REDUCE ID {i + 1}: BY REDUCER {i + 1}: RETURNED FAILED")
            failed_reducers.append(i)
    except grpc.RpcError as e:
        print(f"REDUCE OPERATION FAILED: REDUCE ID {i + 1}: BY REDUCER {i + 1}: RPC ERROR")
        failed_reducers.append(i)
    print("=============================================")

def retry_reduce_operation(idx, itr):
    print(f"RETRYING FAILED REDUCE ID: {idx + 1}")
    idx_success = False
    while(not idx_success):
        for i in range(0, common.REDUCERS):
            try:
                response = reducer_stubs[i].Reduce(kmeans_pb2.reduceInfo(id=idx, iteration=itr))
                if response.success:
                    print(f"REDUCE OPERATION SUCCESSFUL: REDUCE ID {idx + 1}: BY REDUCER {i + 1}")
                    print("UPDATED CENTROIDS BY REDUCER:")
                    for item in response.dict:
                        print(f"{item.key}:({item.value.x},{item.value.y})\n")
                    updated_centroids.append(response.dict)
                    idx_success = True
                    break
                else:
                    print(f"REDUCE OPERATION FAILED: REDUCE ID {idx + 1}: BY REDUCER {i + 1}: RETURNED FAILED")
            except grpc.RpcError as e:
                print(f"REDUCE OPERATION FAILED: REDUCE ID {idx + 1}: BY REDUCER {i + 1}: RPC ERROR")

def run():
    global master_id
    master_id = str(uuid.uuid1())

    global mapper_stubs
    for i in range(0, common.MAPPERS):
        mapper_channel = grpc.insecure_channel(common.master_to_mapper_ports[i])
        mapper_stubs.append(kmeans_pb2_grpc.KMeansStub(mapper_channel))

    global reducer_stubs
    for i in range(0, common.REDUCERS):
        reducer_channel = grpc.insecure_channel(common.master_to_reducer_ports[i])
        reducer_stubs.append(kmeans_pb2_grpc.KMeansStub(reducer_channel))
    
    for i in range(0, common.MAPPERS):
        mapper_chunks.append(read_file_in_chunks(common.input_path, common.MAPPERS, i))

    centroids = []
    print("============= INITIAL CENTROIDS =============")
    centroids = read_entries(common.input_centroids_path)

    #For RANDOM CENTROIDS UNCOMMENT AT EACH RUN
    # for i in range(0, common.CENTROIDS):
    #     x = random.uniform(common.coordinates_from, common.coordinates_to)
    #     y = random.uniform(common.coordinates_from, common.coordinates_to)
    #     centroids.append(kmeans_pb2.coordinate(x=x, y=y))

    for i, item in enumerate(centroids):
            print(f"({item.x:.2f},{item.y:.2f})", end="")
            if i < len(centroids) - 1:
                print(", ", end="")
            else:
                print()
    print("=============================================")

    for itr in range(common.ITERATIONS):
        print(f"=================ITERATION:{itr + 1}=================")

        with concurrent.futures.ThreadPoolExecutor(max_workers=common.MAPPERS) as executor:
            futures = [executor.submit(map_chunk, i, centroids, itr) for i in range(common.MAPPERS)]
            concurrent.futures.wait(futures)
        
        global failed_mappers
        with concurrent.futures.ThreadPoolExecutor(max_workers=common.MAPPERS) as executor:
            futures = [executor.submit(retry_map_chunk, idx, centroids, itr) for idx in failed_mappers]
            concurrent.futures.wait(futures)
        failed_mappers = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=common.REDUCERS) as executor:
            futures = [executor.submit(reduce_operation, i, itr) for i in range(common.REDUCERS)]
            concurrent.futures.wait(futures)

        global failed_reducers
        with concurrent.futures.ThreadPoolExecutor(max_workers=common.REDUCERS) as executor:
            futures = [executor.submit(retry_reduce_operation, idx, itr) for idx in failed_reducers]
            concurrent.futures.wait(futures)
        failed_reducers = []

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

    filename = "data/centroids.txt"
    with open(filename, 'w') as file:
        for i, item in enumerate(centroids):
            if( i != len(centroids) - 1):
                file.write(f"({item.x:.2f},{item.y:.2f}), ")
            else:
                file.write(f"({item.x:.2f},{item.y:.2f})\n")

if __name__ == '__main__':
    original_stdout = sys.stdout
    with open("data/dump/master.txt", 'w') as f:
        sys.stdout = f
        run()
        sys.stdout = original_stdout