# user.py

import zmq


class User:
    def __init__(self, user_id, message_server_ip, message_server_port):
        self.user_id = user_id
        self.message_server_ip = message_server_ip
        self.message_server_port = message_server_port
        self.groups_member = []

    def get_group_list(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(
            f"tcp://{self.message_server_ip}:{self.message_server_port}")

        socket.send_string(f"GROUP LIST REQUEST FROM {self.user_id}")
        group_list = socket.recv_pyobj()
        return group_list

    def join_group(self, group_server_ip, group_server_port, group_id):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{group_server_ip}:{group_server_port}")

        socket.send_string(f"JOIN REQUEST FROM {self.user_id} {group_id}")
        response = socket.recv_pyobj()
        return response

    def leave_group(self, group_server_ip, group_server_port, group_id):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{group_server_ip}:{group_server_port}")

        socket.send_string(f"LEAVE REQUEST FROM {self.user_id} {group_id}")
        response = socket.recv_pyobj()
        return response

    def get_messages(self, group_server_ip, group_server_port, group_id, timestamp):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{group_server_ip}:{group_server_port}")

        socket.send_string(
            f"GET MESSAGE FROM {self.user_id} {group_id} {timestamp}")

        messages = socket.recv_pyobj()
        return messages

    def send_message(self, group_server_ip, group_server_port, group_id, message):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{group_server_ip}:{group_server_port}")

        socket.send_string(
            f"SEND MESSAGE FROM {self.user_id} {group_id} {message}")
        response = socket.recv_pyobj()
        return response


def main_driver(user_id, user):
    

    while True:
        print("\nWelcome to the group messaging app!")
        print("Available options:")
        print("1. List available groups")
        print("2. Join a group")
        print("3. Leave a group")
        print("4. Get messages")
        print("5. Send a message")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            group_list = user.get_group_list()
            print("\nAvailable groups:")
            for group in group_list:
                print(f"IP:-{group[0]}, PORT:-{group[1]}")

        elif choice == "2":

            group_id = input("Enter the group ID/PORT you want to join: ")
            group_server_ip = "127.0.0.1"  # IP address of the group server
            group_server_port = group_id   # Port of the group server


            response = user.join_group(
                group_server_ip, group_server_port, group_id)
            print("Response from group server:", response)
            user.groups_member.append(group_id)

        elif choice == "3":
            print("Group ur part of: ", user.groups_member)
            group_id = input("Enter the group ID/PORT you want to leave: ")
            group_server_ip = "127.0.0.1"  # IP address of the group server
            group_server_port = group_id   # Port of the group server
            response = user.leave_group(
                group_server_ip, group_server_port, group_id)
            print("Response from group server:", response)
            
            if group_id in user.groups_member:
                user.groups_member.remove(group_id)

        elif choice == "4":
            print("Group ur part of: ", user.groups_member)
            group_id = input("Enter the group ID/PORT to get messages from: ")
            timestamp = input(
                "Enter timestamp in %Y-%m-%d %H:%M:%S format otherwise press enter: ")
            group_server_ip = "127.0.0.1"  # IP address of the group server
            group_server_port = group_id  # Port of the group server

            timestamp = None if len(timestamp.strip()) == 0 else timestamp

            response = user.get_messages(
                group_server_ip, group_server_port, group_id, timestamp)
            print("Response from group server:\n", response)

        elif choice == "5":
            print("Group ur part of: ", user.groups_member)
            group_id = input("Enter the group ID/PORT to send a message to: ")
            message = input("Enter your message: ")
            group_server_ip = "127.0.0.1"  # IP address of the group server
            group_server_port = group_id  # Port of the group server
            response = user.send_message(
                group_server_ip, group_server_port, group_id, message)
            print("Response from group server:", response)

        elif choice == "6":
            print("Exiting the app.")
            break

        else:
            print("Invalid choice. Please try again.")
