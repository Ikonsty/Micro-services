from flask import jsonify


class MessageController:
    def __init__(self, message_service, app):
        self.message_service = message_service
        self.app = app

    def index(self):
        print("\tMESSAGES-LOGS: GET request received. Send messages")
        parsed_msgs = " ".join([d["txt"] for d in self.message_service.msgs])
        print(parsed_msgs)
        return jsonify({"msgs": parsed_msgs})

    def register_routes(self):
        self.app.route("/", methods=["GET"])(self.index)
