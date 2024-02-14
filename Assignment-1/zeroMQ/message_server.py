# message_server.py

import zmq


class MessageServer:
    def __init__(self):
        self.group_servers = []

    def handle_join_request(self, ip_address, port):
        self.group_servers.append((ip_address, port))
        return "SUCCESS"

    def handle_group_list_request(self):
        return self.group_servers


def main():
    server = MessageServer()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5000")

    while True:
        message = socket.recv_string()
        print("Received request:", message)

        if message.startswith("GROUP REGISTER REQUEST"):
            grp_server_ip, grp_server_port = message.split()[-2:]
            response = server.handle_join_request(
                grp_server_ip, grp_server_port)

        elif message.startswith("GROUP LIST REQUEST"):
            response = server.handle_group_list_request()

        else:
            response = "Invalid request"

        print(server.group_servers)
        socket.send_pyobj(response)


if __name__ == "__main__":
    main()
