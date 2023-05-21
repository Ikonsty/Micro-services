import uuid
from random import choice
import requests
from json import dumps
from fields import UUIDEncoder
import pika
import os


class FacadeService:
    def __init__(self) -> None:
        # self.loggingServices = [
        #     "http://logging-service-1:8080/logging",
        #     "http://logging-service-2:8081/logging",
        #     "http://logging-service-3:8082/logging",
        # ]
        self.q_name = os.environ.get("Q_NAME")
        self.rabbit_port = os.environ.get("RABBITMQ_PORT")
        self.rabbit_host = os.environ.get("RABBITMQ_HOST")
        self.m_port = os.environ.get("MESSAGES_PORT")
        self.m_host = os.environ.get("MESSAGES_HOST")

        self.messagesServices = [f"http://{self.m_host}:{self.m_port}"]

    def get_messages(self):
        # r_l = requests.get(choice(self.loggingServices))
        # data_l = r_l.content.decode("utf-8")

        r_m = requests.get(choice(self.messagesServices))
        data_m = r_m.content.decode("utf-8")
        print("\tFACADE-LOGS: Received messages")
        return {"msgs": "test"}, data_m  # , data_l

    def send_message(self, msg):
        msg_dict = {"id": uuid.uuid4(), "txt": msg}
        msg_json = dumps(msg_dict, cls=UUIDEncoder)

        # Send the message to Logging
        # r_l = requests.post(choice(self.loggingServices), json=msg_json)

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
