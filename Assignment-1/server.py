import grpc
from concurrent import futures
import shopping_pb2
import shopping_pb2_grpc
import uuid
import bisect

def binary_search(requests, target_id):
    ids = [request.id for request in requests]
    index = bisect.bisect_left(ids, target_id)
    if index < len(ids) and ids[index] == target_id:
        return index
    else:
        return -1

class MarketPlaceServicer(shopping_pb2_grpc.MarketPlaceServicer):
    def __init__(self):
        self.seller_list = []
        self.item_list = []
        self.item_id = 1
    
    def RegisterSeller(self, request, context):
        print(f"Seller join request from {request.seller_address}[ip:port], uuid = {request.seller_uuid}")
        if any(seller.uuid == request.uuid for seller in self.seller_list):
            print("Seller UUID already exists. Register Seller failed.")
            return shopping_pb2.stringReply(reply="FAIL")
        else:
            self.seller_list.append(request)
            print("Seller UUID added to the list.")
            return shopping_pb2.stringReply(reply="SUCCESS")

    def SellItem(self, request, context):
        print(f"Sell Item request from {request.seller_address}[ip:port], uuid = {request.seller_uuid}")
        request.id=self.item_id
        self.item_id+=1
        self.item_list.append(request)
        print("Item added to the market Place :")
        print(self.item_list[-1])
        return shopping_pb2.stringReply(reply="SUCCESS")
    
    def UpdateItem(self, request, context):
        print(f"Update Item: {request.id} request from {request.seller_address}[ip:port], uuid = {request.seller_uuid}")
        result = binary_search(self.item_list, request.id)
        if(result != -1 and self.item_list[result].seller_address == request.seller_address and self.item_list[result].seller_uuid == request.seller_uuid):
            self.item_list[result].price = request.price
            self.item_list[result].quantity = request.quantity
        else:
            print("Authentication failed.")
            return shopping_pb2.stringReply(reply="FAIL")
        print("Item updated to the market Place :")
        print(self.item_list[result])
        #notify buyers code
        return shopping_pb2.stringReply(reply="SUCCESS")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_MarketPlaceServicer_to_server(MarketPlaceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
