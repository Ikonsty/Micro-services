import pika
import time
from json import loads
from consul import Consul
import os


class MessageService:
    def __init__(self, client):
        self.index = str(os.environ.get("MY_INDEX"))
        self.client = client

        self.q_name = None
        self.rabbit_port = None

        while self.rabbit_port == None or self.q_name == None:
            _, self.q_name = self.client.kv.get("Q_NAME")
            _, self.rabbit_port = self.client.kv.get("RABBITMQ_PORT")

        self.q_name = self.q_name["Value"].decode("utf-8")
        self.rabbit_port = self.rabbit_port["Value"].decode("utf-8")
        self.rabbit_host = "rabbitmq"

        print(f"\tMESSAGES: {self.rabbit_port} | {self.q_name}")

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
