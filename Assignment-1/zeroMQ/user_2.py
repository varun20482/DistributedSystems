import user_utility
import uuid

def main():
    user_id = uuid.uuid4()
    message_server_ip = "127.0.0.1"  # IP address of the message server
    message_server_port = "5000"  # Port of the message server

    user = user_utility.User(user_id, message_server_ip, message_server_port)

    user_utility.main_driver(user_id=user_id, user= user)
    
if __name__ == "__main__":
    main()

