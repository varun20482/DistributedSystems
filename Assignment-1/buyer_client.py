import grpc
import shopping_pb2
import shopping_pb2_grpc
import socket
import uuid
import time
import threading

on = True
def notification_thread(stub, global_buyer_uuid):
    while on:
        buyer_notification_message = shopping_pb2.BuyerNotificationRequest(
            buyer_uuid=global_buyer_uuid
        )
        for response in stub.GetBuyerNotifications(buyer_notification_message):
            print("The following item has been updated ...")
            print(response)
        time.sleep(1)

def get_ip_port():
    ip_address = "127.0.0.1"
    port = 50051 
    return f"{ip_address}:{port}"

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = shopping_pb2_grpc.MarketPlaceStub(channel)

    global_buyer_uuid = str(uuid.uuid1())
    global_buyer_addr = get_ip_port()

    register_message = shopping_pb2.BuyerInfo(
        buyer_address = global_buyer_addr,
        buyer_uuid = global_buyer_uuid
    )
    response = stub.RegisterBuyer(register_message)
    print("Registering Buyer with uuid:", register_message.buyer_uuid, "and address:", register_message.buyer_address)
    print(response)

    notification_thread_instance = threading.Thread(target=notification_thread, args=(stub, global_buyer_uuid))
    notification_thread_instance.start()

    while True:
        print("Options:")
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add To Wish List")
        print("4. Rate Item")
        print("5. Logout")
        
        option = input("Enter your choice (1-5): ")
        
        if option == '1':
            print("Option 1: Search Item")
            
            name = input("Enter item name: ")
            category = input("Enter item category (ELECTRONICS, FASHION, OTHERS, ANY): ")
            category_enum = None
            if category == "ELECTRONICS":
                category_enum = shopping_pb2.SearchRequest.ELECTRONICS
            elif category == "FASHION":
                category_enum = shopping_pb2.SearchRequest.FASHION
            elif category == "OTHERS":
                category_enum = shopping_pb2.SearchRequest.OTHERS
            elif category == "ANY":
                category_enum = shopping_pb2.SearchRequest.ANY
            else:
                print("Invalid category input")

            search_message = shopping_pb2.SearchRequest(
            name=name,
            category=category_enum,
            buyer_uuid=global_buyer_uuid,
            buyer_address=global_buyer_addr 
            )
            print("Request sent to search items on the market place...")
            response = stub.SearchItem(search_message)
            print(response)

        elif option == '2':
            print("Option 2: Buy Item")
            id = int(input("Enter item id: "))
            quantity = int(input("Enter item quantity: "))
            buy_message = shopping_pb2.BuyRequest(
            id=id,
            quantity=quantity,
            buyer_address=global_buyer_addr
            )
            print("Request sent to buy item from the market place...")
            response = stub.BuyItem(buy_message)
            print(response)

        elif option == '3':
            print("Option 3: Add to WishList")
            id = int(input("Enter item id: "))
            wishlist_message = shopping_pb2.WishListRequest(
                id=id,
                buyer_address=global_buyer_addr,
                buyer_uuid=global_buyer_uuid
            )
            print("Request sent to add item to wish list to the market place...")
            response = stub.AddToWishList(wishlist_message)
            print(response)

        elif option == '4':
            print("Option 4: Rate Item")
            id = int(input("Enter item id: "))
            rating = int(input("Enter item rating(1-5): "))
            rating_message = shopping_pb2.RateRequest(
                id=id,
                buyer_address=global_buyer_addr,
                rating=rating
            )
            print("Request sent to rate item to the market place...")
            response = stub.RateItem(rating_message)
            print(response)

        elif option == '5':
            print("Logging out...")
            global on
            on = False
            notification_thread_instance.join()
            break
        else:
            print("Invalid option. Please choose again.")


if __name__ == '__main__':
    run()