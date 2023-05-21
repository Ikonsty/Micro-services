import uuid
from random import choice
import requests
from json import dumps
from fields import UUIDEncoder
import pika
import os


class FacadeService:
    def __init__(self) -> None:
        self.q_name = os.environ.get("Q_NAME")
        self.rabbit_port = os.environ.get("RABBITMQ_PORT")
        self.rabbit_host = os.environ.get("RABBITMQ_HOST")
        self.m_port = os.environ.get("MESSAGES_PORT")
        self.m_host = os.environ.get("MESSAGES_HOST")

        self.ls1_host = os.environ.get("LOGGING_HOST_1")
        self.ls2_host = os.environ.get("LOGGING_HOST_2")
        self.ls3_host = os.environ.get("LOGGING_HOST_3")
        self.ls1_port = os.environ.get("LOGGING_PORT_1")
        self.ls2_port = os.environ.get("LOGGING_PORT_2")
        self.ls3_port = os.environ.get("LOGGING_PORT_3")

        self.loggingServices = [
            f"http://{self.ls1_host}:{self.ls1_port}/logging",
            f"http://{self.ls2_host}:{self.ls2_port}/logging",
            f"http://{self.ls3_host}:{self.ls3_port}/logging",
        ]

        self.messagesServices = [f"http://{self.m_host}:{self.m_port}"]

    def get_messages(self):
        r_l = requests.get(choice(self.loggingServices))
        data_l = r_l.content.decode("utf-8")

        r_m = requests.get(choice(self.messagesServices))
        data_m = r_m.content.decode("utf-8")
        print("\tFACADE-LOGS: Received messages")
        return data_l, data_m

    def send_message(self, msg):
        msg_dict = {"id": uuid.uuid4(), "txt": msg}
        msg_json = dumps(msg_dict, cls=UUIDEncoder)

        # Send the message to Logging
        r_l = requests.post(choice(self.loggingServices), json=msg_json)
        print("RESPONSE FROM LOGGING", r_l)

        # Send the message to Messages
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbit_host, self.rabbit_port)
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.q_name)

        channel.basic_publish(exchange="", routing_key=self.q_name, body=msg_json)
        connection.close()
        print(f"\tFACADE-LOGS: Message sent: {msg}")
        return "200 OK", 200
