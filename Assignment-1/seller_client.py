import grpc
import shopping_pb2
import shopping_pb2_grpc
import socket
import uuid
import threading
import time

on = True
def notification_thread(stub, global_seller_uuid):
    global on
    while on:
        seller_notification_message = shopping_pb2.SellerNotificationRequest(
            seller_uuid=global_seller_uuid
        )
        for response in stub.GetSellerNotifications(seller_notification_message):
            print("The following item has been updated ...")
            print(response)
        time.sleep(0.01)

def get_ip_port():
    ip_address = "127.0.0.1"
    port = 50051 
    return f"{ip_address}:{port}"

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = shopping_pb2_grpc.MarketPlaceStub(channel)

    global_seller_uuid = str(uuid.uuid1())
    global_seller_addr = get_ip_port()

    register_message = shopping_pb2.SellerInfo(
        seller_address = global_seller_addr,
        seller_uuid = global_seller_uuid
    )
    response = stub.RegisterSeller(register_message)
    print("Registering Seller with uuid:", register_message.seller_uuid, "and address:", register_message.seller_address)
    print(response)

    notification_thread_instance = threading.Thread(target=notification_thread, args=(stub, global_seller_uuid))
    notification_thread_instance.start()

    while True:
        print("Options:")
        print("1. Sell Item")
        print("2. Update Item")
        print("3. Delete Item")
        print("4. Display Items")
        print("5. Logout")
        
        option = input("Enter your choice (1-5): ")
        
        if option == '1':
            print("Option 1: Sell Item")
            
            name = input("Enter item name: ")
            category = input("Enter item category (ELECTRONICS, FASHION, OTHERS): ")
            category_enum = None
            if category == "ELECTRONICS":
                category_enum = shopping_pb2.Item.ELECTRONICS
            elif category == "FASHION":
                category_enum = shopping_pb2.Item.FASHION
            elif category == "OTHERS":
                category_enum = shopping_pb2.Item.OTHERS
            else:
                print("Invalid category input")
            quantity = int(input("Enter item quantity: "))
            description = input("Enter item description: ")
            price = float(input("Enter item price: "))

            item_message = shopping_pb2.Item(
            name=name,
            category=category_enum, 
            quantity=quantity,
            description=description,
            seller_uuid=global_seller_uuid,
            seller_address=global_seller_addr,
            price=price,
            rating=0,
            total_ratings=0
            )
            print("Request sent to list item on the market place...")
            response = stub.SellItem(item_message)
            print(response)

        elif option == '2':
            print("Option 2: Update Item")

            id = int(input("Enter item id: "))
            quantity = int(input("Enter item quantity: "))
            price = float(input("Enter item price: "))
            seller_uuid=input("Enter seller uuid: ")
            seller_address=input("Enter seller address[ip:port]: ")

            update_message = shopping_pb2.ItemUpdate(
            id=id,
            quantity=quantity,
            seller_uuid=seller_uuid,
            seller_address=seller_address,
            price=price
            )
            print("Request sent to update item on the market place...")
            response = stub.UpdateItem(update_message)
            print(response)

        elif option == '3':
            print("Option 3: Delete Item")
            id = int(input("Enter item id: "))
            seller_uuid=input("Enter seller uuid: ")
            seller_address=input("Enter seller address[ip:port]: ")

            delete_message = shopping_pb2.ItemDelete(
            id=id,
            seller_uuid=seller_uuid,
            seller_address=seller_address,
            )
            print("Request sent to delete item from the market place...")
            response = stub.DeleteItem(delete_message)
            print(response)

        elif option == '4':
            print("Option 4: Display Items")
            display_message = shopping_pb2.SellerInfo(
            seller_address=global_seller_addr,
            seller_uuid=global_seller_uuid,
            )
            print("Request sent to display items from the market place...")
            response = stub.DisplaySellerItems(display_message)
            print(response.items)

        elif option == '5':
            seller_notification_message = shopping_pb2.SellerNotificationRequest(
                seller_uuid=global_seller_uuid
            )
            for response in stub.GetSellerNotifications(seller_notification_message):
                print()
                print("The following item has been updated ...")
                print(response)
            print("Logging out...")
            global on
            on = False
            notification_thread_instance.join()
            break
        else:
            print("Invalid option. Please choose again.")


if __name__ == '__main__':
    run()