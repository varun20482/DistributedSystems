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
        self.buyer_list = []
        self.item_list = []
        self.wish_list = {}
        self.seller_notifications = {}
        self.buyer_notifications = {}
        self.item_id = 1
    
    def RegisterSeller(self, request, context):
        print(f"Seller join request from {request.seller_address}[ip:port], uuid = {request.seller_uuid}")
        if any(seller.seller_uuid == request.seller_uuid for seller in self.seller_list):
            print("Seller UUID already exists. Register Seller failed.")
            print()
            return shopping_pb2.stringReply(reply="FAIL")
        else:
            self.seller_list.append(request)
            print("Seller UUID added to the list.")
            print()
            return shopping_pb2.stringReply(reply="SUCCESS")
        
    def RegisterBuyer(self, request, context):
        print(f"Buyer join request from {request.buyer_address}[ip:port], uuid = {request.buyer_uuid}")
        if any(buyer.buyer_uuid == request.buyer_uuid for buyer in self.buyer_list):
            print("Buyer UUID already exists. Register Buyer failed.")
            print()
            return shopping_pb2.stringReply(reply="FAIL")
        else:
            self.buyer_list.append(request)
            print("Buyer UUID added to the list.")
            print()
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
        if request.id in self.wish_list:
            for buyer_uuid in self.wish_list[request.id]:
                if(buyer_uuid in self.buyer_notifications):
                    self.buyer_notifications[buyer_uuid].append[self.item_list[result]]
                else:
                    self.buyer_notifications[buyer_uuid] = [self.item_list[result]]
        
        print()
        return shopping_pb2.stringReply(reply="SUCCESS")
    
    def DeleteItem(self, request, context):
        print(f"Delete Item: {request.id} request from {request.seller_address}[ip:port], uuid = {request.seller_uuid}")
        result = binary_search(self.item_list, request.id)
        if(result != -1 and self.item_list[result].seller_address == request.seller_address and self.item_list[result].seller_uuid == request.seller_uuid):
            deleted = self.item_list.pop(result)
            print("Item deleted from the market Place :")
            print(deleted)
        else:
            print("Authentication failed.")
            print()
            return shopping_pb2.stringReply(reply="FAIL")
        
        #Delete product from wishlist of user as well
        if request.id in self.wish_list:
            del self.wish_list[request.id]

        print()
        return shopping_pb2.stringReply(reply="SUCCESS")
    
    def DisplaySellerItems(self, request, context):
        print(f"Display Items request from {request.seller_address}[ip:port], uuid = {request.seller_uuid}")
        item_list_message = shopping_pb2.ItemList()
        for item in self.item_list:
            if item.seller_uuid == request.seller_uuid:
                item_list_message.items.append(item)
        print()
        return item_list_message
    
    def SearchItem(self, request, context):
        print(f"Search Items request from {request.buyer_address}[ip:port], uuid = {request.buyer_uuid}")
        item_list_message = shopping_pb2.ItemList()
        for item in self.item_list:
            if request.name == "" or request.name == item.name:
                if request.category == shopping_pb2.SearchRequest.ANY or request.category == item.category:
                    item_list_message.items.append(item)
        print()
        return item_list_message
    
    def BuyItem(self, request, context):
        print(f"Buy request {request.quantity} of item {request.id}, from {request.buyer_address}")
        result = binary_search(self.item_list, request.id)
        if(result != -1):
            if(self.item_list[result].quantity >= request.quantity):
                self.item_list[result].quantity-=request.quantity
            else:
                print("Out of Stock.")
                return shopping_pb2.stringReply(reply="FAIL")
        else:
            print("Invalid Product Id.")
            return shopping_pb2.stringReply(reply="FAIL")
        print("Product purchased.")
        print(self.item_list[result])
        print()

        #notify seller
        if(self.item_list[result].seller_uuid in self.seller_notifications):
            self.seller_notifications[self.item_list[result].seller_uuid].append(self.item_list[result])
        else:
            self.seller_notifications[self.item_list[result].seller_uuid] = [self.item_list[result]]

        return shopping_pb2.stringReply(reply="SUCCESS")
    
    def AddToWishList(self, request, context):
        print(f"Wishlist request of item {request.id}, from {request.buyer_address}")
        result = binary_search(self.item_list, request.id)
        if(result != -1):
            if(request.id in self.wish_list):
                self.wish_list[request.id].add(request.buyer_uuid)
            else:
                self.wish_list[request.id] = {request.buyer_uuid}
        else:
            print("Invalid Product Id.")
            print()
            return shopping_pb2.stringReply(reply="FAIL")
        
        print("Added to wishlist.")
        print(self.wish_list)
        print()
        return shopping_pb2.stringReply(reply="SUCCESS")
    
    def RateItem(self, request, context):
        print(f"{request.buyer_address} rated item {request.id} with {request.rating} stars.")
        result = binary_search(self.item_list, request.id)
        if(result != -1):
            self.item_list[result].rating = (self.item_list[result].rating * self.item_list[result].total_ratings + request.rating) / (self.item_list[result].total_ratings + 1)
            self.item_list[result].total_ratings += 1
        else:
            print("Invalid Product Id.")
            return shopping_pb2.stringReply(reply="FAIL")
        print("Rated Item.")
        print(self.item_list[result])
        print()
        return shopping_pb2.stringReply(reply="SUCCESS")
    
    def GetBuyerNotifications(self, request, context):
        if request.buyer_uuid in self.buyer_notifications:
            for item in self.buyer_notifications[request.buyer_uuid]:
                yield item
            del self.buyer_notifications[request.buyer_uuid]
    
    def GetSellerNotifications(self, request, context):
        if request.seller_uuid in self.seller_notifications:
            for item in self.seller_notifications[request.seller_uuid]:
                yield item
            del self.seller_notifications[request.seller_uuid]
        
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_MarketPlaceServicer_to_server(MarketPlaceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Received Ctrl+C. Shutting down the server gracefully...")
        server.stop(None)

if __name__ == '__main__':
    serve()
