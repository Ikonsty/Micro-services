import uuid
from random import choice
import requests
from json import dumps
from fields import UUIDEncoder
import pika
import os
from consul import Consul
from dns.resolver import Resolver, NoAnswer, DNSException


class FacadeService:
    def __init__(self) -> None:
        self.q_name = os.environ.get("Q_NAME")
        self.rabbit_port = os.environ.get("RABBITMQ_PORT")
        self.rabbit_host = os.environ.get("RABBITMQ_HOST")
        self.consul_port = os.environ.get("CONSUL_PORT")
        self.consul_host = os.environ.get("CONSUL_HOST")

        # self.ls1_host = os.environ.get("LOGGING_HOST_1")
        # self.ls2_host = os.environ.get("LOGGING_HOST_2")
        # self.ls3_host = os.environ.get("LOGGING_HOST_3")
        # self.ls1_port = os.environ.get("LOGGING_PORT_1")
        # self.ls2_port = os.environ.get("LOGGING_PORT_2")
        # self.ls3_port = os.environ.get("LOGGING_PORT_3")

        self.loggingServices = [
            f"http://consul-client-messages.service.consul:8600/logging"
            # f"http://{self.ls1_host}:{self.ls1_port}/logging",
            # f"http://{self.ls2_host}:{self.ls2_port}/logging",
            # f"http://{self.ls3_host}:{self.ls3_port}/logging",
        ]

    def get_messages(self):
        # r_l = requests.get(choice(self.loggingServices))
        # data_l = r_l.content.decode("utf-8")

        try:
            m_host, m_port = self.get_messages_host_port()
            r_m = requests.get(f"http://{m_host}:{m_port}/logging")
            data_m = r_m.content.decode("utf-8")
        except:
            print("Enable to resolve Messages DNS")
            data_m = None
        print("\tFACADE-LOGS: Received messages")
        return "empty", data_m  # data_l, data_m

    def send_message(self, msg):
        msg_dict = {"id": uuid.uuid4(), "txt": msg}
        msg_json = dumps(msg_dict, cls=UUIDEncoder)

        # Send the message to Logging
        # r_l = requests.post(choice(self.loggingServices), json=msg_json)
        # print("RESPONSE FROM LOGGING", r_l)

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

    def get_messages_host_port(self):
        # Set up the Consul DNS resolver
        resolver = Resolver()
        resolver.port = self.consul_port
        resolver.nameservers = [self.consul_host]

        # Specify the service name and domain
        service_name = "consul-client-messages"
        domain = "service.consul"

        # Formulate the DNS query for SRV record
        query = f"_{service_name}._{domain}"

        # Perform the DNS query for SRV record
        try:
            answer = resolver.query(query, rdtype="SRV")
            for srv_record in answer:
                host = srv_record.target.to_text().rstrip(".")
                port = srv_record.port
                return host, port
        except NoAnswer:
            print(f"No SRV record found for {query}")
            return None
        except DNSException as e:
            print(f"DNS query failed: {e}")
            return None
