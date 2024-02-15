import pika
import sys

class User:
    def __init__(self, name):
        self.user_name = name
        credentials = pika.PlainCredentials('sam', 'sam')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue=self.user_name)

    def update_subscription(self, youtuber_name, action):
        message = {
            "user": self.user_name,
            "youtuber": youtuber_name,
            "subscribe": action
        }
        self.channel.basic_publish(exchange='', routing_key='user_requests', body=str(message))
        print("SUCCESS: Subscription updated")

    def receive_notifications(self):
        def callback(ch, method, properties, body):
            print(body.decode())

        self.channel.basic_consume(queue=self.user_name, on_message_callback=callback, auto_ack=True)
        print("Waiting for notifications...")
        self.channel.start_consuming()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python User.py <UserName> [s/u <YoutuberName>]")
        sys.exit(1)

    user_name = sys.argv[1]
    user = User(user_name)

    # Start receiving notifications in a separate process
    import multiprocessing
    notification_process = multiprocessing.Process(target=user.receive_notifications)
    notification_process.start()

    if len(sys.argv) > 2:
        action = sys.argv[2]
        if action not in ['s', 'u']:
            print("Invalid action. Use 's' for subscribe or 'u' for unsubscribe.")
            sys.exit(1)
        if len(sys.argv) < 4:
            print("Please provide YoutuberName for subscription/unsubscription.")
            sys.exit(1)
        youtuber_name = sys.argv[3]
        user.update_subscription(youtuber_name, action)
