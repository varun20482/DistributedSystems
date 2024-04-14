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
    def __init__(self):
        self.id = int(sys.argv[1])

    def Map(self, request, context):
        print(f"==== MAP ID: {self.id} REQUEST FROM MASTER ====")
        for i in range(0, common.REDUCERS):
            filename = f"mappers/M{int(sys.argv[1]) + 1}/partition_{i + 1}.txt"
            with open(filename, 'w') as file:
                file.write("")
        start_index = request.indices.start_index
        end_index = request.indices.end_index
        data_points = read_entries(common.input_path, start_index, end_index)

        print("=========== ASSIGNED POINTS ============")
        for i, item in enumerate(data_points):
            print(f"({item.x:.2f},{item.y:.2f})", end="")
            if i < len(data_points) - 1:
                print(", ", end="")
            else:
                print()
        print("========================================")

        centroids = request.centroids

        print("========== ASSIGNED CENTROIDS ==========")
        for i, item in enumerate(centroids):
            print(f"({item.x:.2f},{item.y:.2f})", end="")
            if i < len(centroids) - 1:
                print(", ", end="")
            else:
                print()
        print("========================================")

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

        print("============= MAPPED RESULT ============")
        for i, item in enumerate(dict):
                    print(f"{item.key}:({item.value.x},{item.value.y})\n")
                    if i < len(dict) - 1:
                        print(", ", end="")
                    else:
                        print()
        print("========================================")

        response = self.Partition(kmeans_pb2.keyValDict(dict = dict))
        print("========================================")
        return kmeans_pb2.reply(success=True)

    def Partition(self, request):
        print(f"== PARTITION ID:{self.id} REQUEST FROM MAPPER ==")
        dict = sorted(request.dict, key=get_coordinates)
        for item in dict:
            reducer_id = item.key % common.REDUCERS

            print(f"REDUCER ID: {reducer_id} ASSIGNED:")
            print(f"{item.key}:({item.value.x},{item.value.y})\n")

            filename = f"mappers/M{int(sys.argv[1]) + 1}/partition_{reducer_id + 1}.txt"
            with open(filename, 'a') as file:
                file.write(f"{item.key}:({item.value.x},{item.value.y})\n")
        print("========================================")
        return kmeans_pb2.reply(success=True)
    
    def GetPartition(self, request, context):
        print("=========GET PARTITION REQUEST==========")
        print(f"TO MAPPER ID:{self.id}")
        print(f"FROM REDUCER ID:{request.id}")
        dict = []
        filename = f"mappers/M{self.id+1}/partition_{request.id + 1}.txt"
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = int(parts[0])
                        x, y = parts[1].strip('()').split(',')
                        x = float(x)
                        y = float(y)
                        point = kmeans_pb2.coordinate(x=x, y=y)
                        dict.append(kmeans_pb2.keyVal(key = key, value = point))
        print("RETURNED PARTITION")
        for item in dict:
            print(f"{item.key}:({item.value.x},{item.value.y})\n")
        print("========================================")
        return kmeans_pb2.keyValDict(dict = dict)

def serve():
    directory = 'mappers/M' + str(int(sys.argv[1]) + 1)
    if not os.path.exists(directory):
        os.makedirs(directory)
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
    original_stdout = sys.stdout
    with open(f"dump/mapper_{int(sys.argv[1])}.txt", 'w') as f:
        sys.stdout = f
        serve()
        sys.stdout = original_stdout