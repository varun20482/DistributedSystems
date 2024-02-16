import pika
import sys

class Youtuber:
    def __init__(self, name):
        self.youtuber_name = name
        credentials = pika.PlainCredentials('guest', 'guest')
        # credentials = pika.PlainCredentials('sam', 'sam')
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters('35.194.24.139',5672,'/',credentials))

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='youtuber_requests')

    def publish_video(self, video_name):
        message = f"{self.youtuber_name}:{video_name}"
        self.channel.basic_publish(exchange='', routing_key='youtuber_requests', body=message)
        print("SUCCESS: Video published")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)

    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])
    
    youtuber = Youtuber(youtuber_name)
    youtuber.publish_video(video_name)
