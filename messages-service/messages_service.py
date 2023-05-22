import pika
import time
from json import loads


class MessageService:
    def __init__(self, q_name, rabbit_host, rabbit_port):
        self.q_name = q_name
        self.rabbit_host = rabbit_host
        self.rabbit_port = rabbit_port
        self.no_connection = True
        self.connection = None
        self.channel = None
        self.msgs = []

    def connect_to_rabbitmq(self):
        while self.no_connection:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(self.rabbit_host, self.rabbit_port)
                )
                self.no_connection = False
                print("\tMESSAGES-LOGS: RabbitMQ Connected")
            except:
                print("\tMESSAGES-LOGS: RabbitMQ no connection")
                time.sleep(5)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.q_name)

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        self.msgs.append(loads(body))
        print(f"\tMESSAGES-LOGS: Received {body}")

    def consume_messages(self):
        self.connect_to_rabbitmq()
        self.channel.basic_consume(
            queue=self.q_name, on_message_callback=self.callback, auto_ack=True
        )
        print("\tMESSAGES-LOGS: Waiting for messages")
        self.channel.start_consuming()
