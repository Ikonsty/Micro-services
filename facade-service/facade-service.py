from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal, fields
import uuid
import os
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
        r_l = requests.get(f"http://logging-service:5001/logging")
        r_m = requests.get(f"http://messages-service:5002/messages")
        print("\tFACADE-LOGS: Received messages")
        data_l = r_l.json()
        data_m = r_m.json()
        return marshal({"msgs": data_l["msgs"] + ' | ' + data_m["msgs"]}, msgFields)

    def post(self):
        args = self.reqparse.parse_args()
        msg = {
            "uuid": uuid.uuid4().hex,
            "msg": args["msg"]
        }
        r = requests.post(f"http://logging-service:5001/logging", json=msg)
        print(f"\tFACADE-LOGS: Message sent: {msg}")
        return r.json()

api.add_resource(Facade, "/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)