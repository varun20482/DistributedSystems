import pika
import json
import multiprocessing
import signal
import sys
import os

# File path for subscribers JSON file
SUBSCRIBERS_FILE = 'subscribers.json'

def load_subscribers():
    """Load subscribers from JSON file."""
    try:
        with open(SUBSCRIBERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}
    except json.decoder.JSONDecodeError:
        # If the file is empty or not properly formatted, return an empty dictionary
        return {}
def save_subscribers(subscribers):
    """Save subscribers to JSON file."""
    # Convert sets to lists
    subscribers_copy = {key: list(value) for key, value in subscribers.items()}
    with open(SUBSCRIBERS_FILE, 'w') as file:
        json.dump(subscribers_copy, file)


def consume_user_requests(subscribers, connection, channel):
    def callback(ch, method, properties, body):
        print("Received user request:", body.decode())
        user_data = json.loads(body.decode().replace("'", '"'))
        
        user_name = user_data['user']
        print(f"{user_name} logged in")
        if 'subscribe' in user_data:
            youtuber_name = user_data['youtuber']
            action = user_data['subscribe']

            if action == 's':
                subscribe_user(user_name, youtuber_name, subscribers)
            elif action == 'u':
                unsubscribe_user(user_name, youtuber_name, subscribers)
            else:
                print("Invalid action:", action)
        else:
            print(f"{user_name} logged in")

    try:
        channel.basic_consume(queue='user_requests', on_message_callback=callback, auto_ack=True)
        print("Waiting for user requests...")
        channel.start_consuming()
    except KeyboardInterrupt:
        save_subscribers(subscribers)
        close_connection(connection)

def consume_youtuber_requests(subscribers, connection, channel):
    def callback(ch, method, properties, body):
        youtuber_name, video_name = body.decode().split(':')
        print(f"{youtuber_name} uploaded {video_name}")
        notify_users(youtuber_name, video_name, subscribers)

    channel.basic_consume(queue='youtuber_requests', on_message_callback=callback, auto_ack=True)
    print("Waiting for youtuber requests...")
    channel.start_consuming()

def send_notification(user, notification):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=user)
    channel.basic_publish(exchange='', routing_key=user, body=notification)
    print(f"Notification sent to {user}")
    connection.close()

def notify_users(youtuber_name, video_name, subscribers):
    # print("youtuber_user_list: ", subscribers)
    subscribers = load_subscribers()  # Load subscribers from the JSON file
    if youtuber_name in subscribers:
        subscribers_for_youtuber = subscribers[youtuber_name]
        for user in subscribers_for_youtuber:
            notification = f"New Notification: {youtuber_name} uploaded {video_name}"
            send_notification(user, notification)

def subscribe_user(user_name, youtuber_name, subscribers):
    if youtuber_name not in subscribers:
        subscribers[youtuber_name] = set()
    subscribers[youtuber_name].add(user_name)
    # print("subscriber_user_list after subscription:", subscribers)
    print(f"{user_name} subscribed to {youtuber_name}")
    save_subscribers(subscribers)  # Update subscribers in the JSON file

def unsubscribe_user(user_name, youtuber_name, subscribers):
    if youtuber_name in subscribers and user_name in subscribers[youtuber_name]:
        subscribers[youtuber_name].remove(user_name)
        print(f"{user_name} unsubscribed from {youtuber_name}")
        save_subscribers(subscribers)  # Update subscribers in the JSON file
    else:
        print(f"{user_name} was not subscribed to {youtuber_name}")

def close_connection(connection):
    connection.close()

def user_requests(subscribers_queue):
    subscribers = load_subscribers()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600))
    channel = connection.channel()
    channel.queue_declare(queue='user_requests')

    consume_user_requests(subscribers, connection, channel)

def youtuber_requests(subscribers_queue):
    subscribers = load_subscribers()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600))
    channel = connection.channel()
    channel.queue_declare(queue='youtuber_requests')

    consume_youtuber_requests(subscribers, connection, channel)

if __name__ == '__main__':
    # Create subscribers JSON file if it doesn't exist
    if not os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'w') as file:
            json.dump({}, file)

    user_subscribers_queue = multiprocessing.Queue()
    youtuber_subscribers_queue = multiprocessing.Queue()
    user_subscribers_queue.put(True)
    youtuber_subscribers_queue.put(True)
    
    user_process = multiprocessing.Process(target=user_requests, args=(user_subscribers_queue,))
    user_process.start()

    youtuber_process = multiprocessing.Process(target=youtuber_requests, args=(youtuber_subscribers_queue,))
    youtuber_process.start()

    # Register signal handlers to gracefully terminate the processes
    def signal_handler(sig, frame):
        user_process.terminate()
        youtuber_process.terminate()
        with open(SUBSCRIBERS_FILE, 'w') as file:
            json.dump({}, file)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait for the processes to finish
    user_process.join()
    youtuber_process.join()
