import common
import grpc
import kmeans_pb2
import kmeans_pb2_grpc
import random

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
    print("==============================CENTROIDS==============================")
    for i in range(0, common.CENTROIDS):
        x = random.uniform(common.coordinates_from, common.coordinates_to)
        y = random.uniform(common.coordinates_from, common.coordinates_to)
        centroids.append(kmeans_pb2.coordinate(x=x, y=y))
    print("=====================================================================")

    map_responses = []
    #parallelise this for loop
    for i in range(0, common.MAPPERS):
        print(f"==============================MAPPER_{i}==============================")
        response = mapper_stubs[i].Map(kmeans_pb2.mapInfo(indices=mapper_chunks[i], centroids=centroids))
        map_responses.append(response)
        for item in response.dict:
            print("Key:",item.key,"Value:", item.value)
        print("====================================================================")
    
    for i in range(0, common.MAPPERS):
        print(f"==============================MAPPER_{i}==============================")
        response = mapper_stubs[i].Partition(map_responses[i])
        print(response)
        print("====================================================================")

if __name__ == '__main__':
    run()