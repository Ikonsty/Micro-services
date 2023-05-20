import uuid
from random import choice
import requests
from json import dumps
from fields import UUIDEncoder
from kafka import KafkaProducer


class FacadeService:
    def __init__(self) -> None:
        self.loggingServices = [
            f"http://logging-service-1:8080/logging",
            f"http://logging-service-2:8081/logging",
            f"http://logging-service-3:8082/logging",
        ]

        self.messagesServices = [
            "http://messages-service:5002/messages",
            "http://messages-service:5003/messages'",
            "http://messages-service:5004/messages",
        ]
        self.kafka_bootstrap_servers = ["broker:9092"]

    def get_messages(self):
        r_l = requests.get(choice(self.loggingServices))
        r_m = requests.get(choice(self.messagesServices))
        print("\tFACADE-LOGS: Received messages")
        data_l = r_l.content.decode("utf-8")
        data_m = r_m.json()
        return data_l, data_m

    def send_message(self, msg):
        msg_dict = {"id": uuid.uuid4(), "txt": msg}

        msg_json = dumps(msg_dict, cls=UUIDEncoder)
        r = requests.post(choice(self.loggingServices), json=msg_json)
        print(r)
        print(f"\tFACADE-LOGS: Message sent: {msg}")

        # Send the message to Kafka
        producer = KafkaProducer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_serializer=lambda v: dumps(v).encode("utf-8"),
        )

        producer.send("common_msg", value=msg_dict)
        producer.flush()
        producer.close()
        print(f"\tMESSAGES-LOGS: Message sent: {msg}")

        return r.status_code
