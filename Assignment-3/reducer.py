import common
import grpc
from concurrent import futures
import kmeans_pb2
import kmeans_pb2_grpc
import sys
import os

class KMeansServicer(kmeans_pb2_grpc.KMeansServicer):
    def __init__(self):
        self.id = int(sys.argv[1])
        self.mapper_stubs = []
        for i in range(0, common.MAPPERS):
            mapper_channel = grpc.insecure_channel(common.master_to_mapper_ports[i])
            self.mapper_stubs.append(kmeans_pb2_grpc.KMeansStub(mapper_channel))

    def ShuffleSort(self, partitions):
        data = {}
        for partition in partitions:
            for item in partition:
                if(item.key not in data):
                    data[item.key] = [item.value]
                else:
                    data[item.key].append(item.value)
        return data
    
    def Reduce(self, request, context):
        assigned_tasks = []
        for i in range(0, common.MAPPERS):
            response = self.mapper_stubs[i].GetPartition(kmeans_pb2.reduceInfo(id = request.id))
            assigned_tasks.append(response.dict)
        data = self.ShuffleSort(assigned_tasks)
        centroids = []
        for key in data:
            sum_x = 0
            sum_y = 0
            for point in data[key]:
                sum_x += point.x
                sum_y += point.y
            avg_x = sum_x / len(data[key])
            avg_y = sum_y / len(data[key])
            centroids.append(kmeans_pb2.keyVal(key = key, value = kmeans_pb2.coordinate(x = avg_x, y = avg_y)))
        return kmeans_pb2.keyValDict(dict = centroids)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kmeans_pb2_grpc.add_KMeansServicer_to_server(KMeansServicer(), server)
    server.add_insecure_port(common.reducer_ports[int(sys.argv[1])])
    server.start()
    print("Server started. Listening on port", common.reducer_ports[int(sys.argv[1])])

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Received Ctrl+C. Shutting down the server gracefully...")
        server.stop(None)

if __name__ == '__main__':
    serve()