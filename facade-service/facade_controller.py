from flask_restful import reqparse, marshal
from facade_service import FacadeService
from fields import msgFields
import os
from consul import Consul


class FacadeController:
    def __init__(self, app) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("msg", type=str, location="json")

        cl = self.register_consul()
        self.facade_service = FacadeService(cl)
        self.app = app

        super(FacadeController, self).__init__()

    def get(self):
        data_l, data_m = self.facade_service.get_messages()
        print("GOT:", data_l)
        print("GOT:", data_m)
        return marshal({"msgs": "".join(data_l) + " | " + "".join(data_m)}, msgFields)

    def post(self):
        args = self.reqparse.parse_args()
        status_code = self.facade_service.send_message(args["msg"])
        return status_code

    def register_routes(self):
        self.app.route("/", methods=["GET"])(self.get)
        self.app.route("/", methods=["POST"])(self.post)

    def register_consul(self):
        self.client = Consul(host="consul-server")
        self.client.agent.service.register(
            name=os.environ.get("APP_NAME"),
            port=int(os.environ.get("PORT")),
            address="facade-service",
        )
        return self.client
