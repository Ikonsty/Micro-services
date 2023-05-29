from flask import jsonify
import os
from consul import Consul
from messages_service import MessageService


class MessageController:
    def __init__(self, app):
        cl = self.register_consul()
        self.message_service = MessageService(cl)
        self.app = app

    def get(self):
        print("\tMESSAGES-LOGS: GET request received. Send messages")
        parsed_msgs = " ".join([d["txt"] for d in self.message_service.msgs])
        print(parsed_msgs)
        return jsonify({"msgs": parsed_msgs})

    def register_routes(self):
        self.app.route("/messages", methods=["GET"])(self.get)

    def get_service(self):
        return self.message_service

    def register_consul(self):
        self.client = Consul(host="consul-server")
        index = os.environ.get("MY_INDEX")
        name = os.environ.get("APP_NAME") + index

        self.client.agent.service.register(
            name=name,
            port=int(os.environ.get("PORT")),
            address=f"messages-service-{index}",
        )
        return self.client
