import grpc
import raft_pb2
import raft_pb2_grpc
import threading
import time
import server_info


def run():
    channel = grpc.insecure_channel(server_info.available_servers[server_info.leader_id])
    stub = raft_pb2_grpc.RaftStub(channel)

    while True:
        print("Options:")
        print("1. SET")
        print("2. GET")
        print("3. Exit")

        option = input("Enter your choice: ")
        action_string = ""
        if option == "1":
            variable_name = input("Enter the variable name: ")
            value = input("Enter the value for variable {}: ".format(variable_name))
            action_string = "SET {} {}".format(variable_name, value)
            print("SET {} {}".format(variable_name, value))
            client_message = raft_pb2.ServeClientArgs(Request = action_string)
            try:
                response = stub.ServeClient(client_message)
            except grpc.RpcError as e:
                print("CLIENT: Node down, request unable to send request to", server_info.leader_id)
                server_info.leader_id += 1
                server_info.leader_id %= server_info.N
                print("CLIENT: Leader updated to", server_info.leader_id)
                continue

            if(response.LeaderID != server_info.leader_id):
                print("Incorrect Leader Information.")
                server_info.leader_id = response.LeaderID
                channel = grpc.insecure_channel(server_info.available_servers[response.LeaderID])
                stub = raft_pb2_grpc.RaftStub(channel)
                print("Updated successfully.")
            print(response)
            
        elif option == "2":
            variable_name = input("Enter the variable name: ")
            action_string = "GET " + variable_name
            print("GET", variable_name)
            client_message = raft_pb2.ServeClientArgs(Request = action_string)
            try:
                response = stub.ServeClient(client_message)
            except grpc.RpcError as e:
                print("CLIENT: Node down, request unable to send request to", server_info.leader_id)
                server_info.leader_id += 1
                server_info.leader_id %= server_info.N
                print("CLIENT: Leader updated to", server_info.leader_id)
                continue
            
            if(response.LeaderID != server_info.leader_id):
                print("Incorrect Leader Information.")
                server_info.leader_id = response.LeaderID
                channel = grpc.insecure_channel(server_info.available_servers[response.LeaderID])
                stub = raft_pb2_grpc.RaftStub(channel)
                print("Updated successfully.")
            print(response)

        elif option == "3":
            break

        else:
            print("Invalid option.")

if __name__ == '__main__':
    run()