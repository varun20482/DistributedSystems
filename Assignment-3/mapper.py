import common
import grpc
from concurrent import futures
import kmeans_pb2
import kmeans_pb2_grpc
import sys
import math
import os

def read_entries(filename, start_index, end_index):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()[start_index:end_index]  

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

def get_coordinates(key_val):
    return key_val.key

def distance(point1, point2):
    x1 = point1.x
    y1 = point1.y

    x2 = point2.x
    y2 = point2.y

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

class KMeansServicer(kmeans_pb2_grpc.KMeansServicer):
    def __int__(self):
        self.id = int(sys.argv[1])

    def Map(self, request, context):
        start_index = request.indices.start_index
        end_index = request.indices.end_index
        data_points = read_entries(common.input_path, start_index, end_index)
        centroids = request.centroids
        dict = []
        for point in data_points:
            nearest_centroid = -1
            current_distance = -1
            for key in range(0, len(centroids)):
                cent = centroids[key]
                temp = distance(point, cent)
                if(nearest_centroid == -1 or temp < current_distance):
                    nearest_centroid = key
                    current_distance = temp
            dict.append(kmeans_pb2.keyVal(key = nearest_centroid, value = point))   
        return kmeans_pb2.returnMap(dict = dict)

    def Partition(self, request, context):
        dict = sorted(request.dict, key=get_coordinates)
        last_key = -1
        reducer_id = -1
        for item in dict:
            if(last_key == -1 or last_key != item.key):
                reducer_id += 1
                reducer_id %= common.REDUCERS
            filename = f"mappers/M{int(sys.argv[1]) + 1}/partition_{reducer_id + 1}.txt"
            with open(filename, 'a') as file:
                file.write(f"{item.key}:({item.value.x},{item.value.y})\n")
            last_key = item.key
        return kmeans_pb2.reply(success=True)

def serve():
    directory = 'mappers/M' + str(int(sys.argv[1]) + 1)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(0, common.REDUCERS):
        filename = f"mappers/M{int(sys.argv[1]) + 1}/partition_{i + 1}.txt"
        print(filename)
        with open(filename, 'w') as file:
            file.write("")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kmeans_pb2_grpc.add_KMeansServicer_to_server(KMeansServicer(), server)
    server.add_insecure_port(common.mapper_ports[int(sys.argv[1])])
    server.start()
    print("Server started. Listening on port", common.mapper_ports[int(sys.argv[1])])

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Received Ctrl+C. Shutting down the server gracefully...")
        server.stop(None)

if __name__ == '__main__':
    serve()