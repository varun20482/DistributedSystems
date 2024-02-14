# group_server.py

import zmq
import datetime
import threading


class GroupServer:
    def __init__(self):
        self.grp_messages = []
        self.user_tele = []

    def join_group(self, user_id):
        if user_id not in self.user_tele:
            self.user_tele.append(user_id)
            return "SUCCESS"
        else:
            return "ALREADY PART OF THIS GROUP!"

    def leave_group(self, user_id):
        if user_id in self.user_tele:
            self.user_tele.remove(user_id)
            return "SUCCESS"
        else:
            return "User not found in this group"

    def get_messages(self, user_id, timestamp):
        print(user_id, timestamp)

        if user_id not in self.user_tele:
            return "User not in group"

        if timestamp != "None":
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            relevant_messages = []
            for msg in self.grp_messages:
                if msg[0] >= timestamp:
                    relevant_messages.append(msg)
        else:
            relevant_messages = self.grp_messages

        return relevant_messages

    def send_message(self, user_id, message):
        if user_id in self.user_tele:
            timestamp = datetime.datetime.now()
            self.grp_messages.append((timestamp, user_id, message))
            return "SUCCESS"
        else:
            return "User not in group"


def register_group(group_server_ip, group_server_port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://34.29.92.77:5000")

    socket.send_string(
        f"GROUP REGISTER REQUEST FROM Group -> IP:PPORT {group_server_ip} {group_server_port}")
    response = socket.recv_pyobj()
    print("Response from message server: ", response)


def server_control(port):

    server = GroupServer()
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

    while True:
        message = socket.recv_string()
        print(f"Received request on group {port} :", message)

        if message.startswith("JOIN REQUEST"):
            user_id = message.split()[-2]
            response = server.join_group(user_id)

        elif message.startswith("LEAVE REQUEST"):
            user_id = message.split()[-2]
            response = server.leave_group(user_id)

        elif message.startswith("GET MESSAGE"):
            user_id = message.split()[3]
            timestamp = ' '.join(message.split()[5:])
            response = server.get_messages(user_id, timestamp)

        elif message.startswith("SEND MESSAGE"):
            user_id = message.split()[3]
            sent_message = ' '.join(message.split()[5:])
            response = server.send_message(user_id, sent_message)
        else:
            response = "Invalid request"

        print(server.user_tele)
        socket.send_pyobj(response)


# Start a server for each port
ports = [5555, 5556]  # List of ports or number of groups


def main():

    for port in ports:
        register_group("127.0.0.1", port)

    for port in ports:
        t = threading.Thread(target=server_control, args=(port,))
        t.start()


if __name__ == "__main__":
    main()
