import uuid
from random import choice
import requests
from json import dumps
from fields import UUIDEncoder
import pika
import os
from base64 import b64decode


class FacadeService:
    def __init__(self, client):
        self.client = client
        print("SERVICES", self.client.agent.services())
        self.msg1_host = self.client.agent.services()["messagesService1"]["Address"]
        self.msg2_host = self.client.agent.services()["messagesService2"]["Address"]
        self.msg3_host = self.client.agent.services()["messagesService3"]["Address"]
        self.msg1_port = self.client.agent.services()["messagesService1"]["Port"]
        self.msg2_port = self.client.agent.services()["messagesService2"]["Port"]
        self.msg3_port = self.client.agent.services()["messagesService3"]["Port"]
        self.ls1_port = os.environ.get("LS1_PORT")
        self.ls2_port = os.environ.get("LS2_PORT")
        self.ls3_port = os.environ.get("LS3_PORT")

        self.q_name = None
        self.rabbit_port = None

        while self.rabbit_port == None or self.q_name == None:
            _, self.q_name = self.client.kv.get("Q_NAME")
            _, self.rabbit_port = self.client.kv.get("RABBITMQ_PORT")

        self.q_name = self.q_name["Value"].decode("utf-8")
        self.rabbit_port = self.rabbit_port["Value"].decode("utf-8")
        self.rabbit_host = "rabbitmq"

        self.loggingServices = [
            f"http://logging-service-1:{self.ls1_port}/logging",
            f"http://logging-service-2:{self.ls2_port}/logging",
            f"http://logging-service-3:{self.ls3_port}/logging",
        ]
        self.messagesService = [
            f"http://{self.msg1_host}:{self.msg1_port}/messages",
            f"http://{self.msg2_host}:{self.msg2_port}/messages",
            f"http://{self.msg3_host}:{self.msg3_port}/messages",
        ]

    def get_messages(self):
        r_l = requests.get(choice(self.loggingServices))
        data_l = r_l.content.decode("utf-8")

        r_m = requests.get(choice(self.messagesService))
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
