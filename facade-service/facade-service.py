from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal, fields
import uuid
from random import choice
import requests
import json


msgFields = {
    "msgs": fields.String
}

app = Flask(__name__)
api = Api(app)

class Facade(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("msg", type=str, location="json")

        super(Facade, self).__init__()

    def get(self):
        loggingServices = [f"http://logging-service-1:8080/logging",
                           f"http://logging-service-2:8081/logging",
                           f"http://logging-service-3:8082/logging"] 
        r_l = requests.get(choice(loggingServices))
        r_m = requests.get(f"http://messages-service:5002/messages")
        print("\tFACADE-LOGS: Received messages")
        data_l = r_l.content.decode('utf-8')
        data_m = r_m.json()
        print("GOT:", data_l)
        print("GOT:", data_m)
        return marshal({"msgs": '[' + ''.join(data_l) + '] ' + ' | ' + data_m["msgs"]}, msgFields)

    def post(self):
        args = self.reqparse.parse_args()
        msg = {
            "id": uuid.uuid4(),
            "txt": args["msg"]
        }

        msg = json.dumps(msg, cls=UUIDEncoder)

        loggingServices = [f"http://logging-service-1:8080/logging",
                           f"http://logging-service-2:8081/logging",
                           f"http://logging-service-3:8082/logging"]
        r = requests.post(choice(loggingServices), json=msg)
        print(r)
        print(f"\tFACADE-LOGS: Message sent: {msg}")
        return r.status_code

api.add_resource(Facade, "/")

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
