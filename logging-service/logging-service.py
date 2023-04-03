from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal, fields


messages = {'9fe2c4e93f654fdbb24c02b15259716c': "Hello, world",
            '9fe2c4e93f654fdbb24c92b15159716c': "Another line"}

msgFields = {
    "uuid": fields.String,
    "msg": fields.String
}


app = Flask(__name__)
api = Api(app) 


class Logging(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("uuid", type=str, required=True,
            help="The message must be provided", location="json")
        self.reqparse.add_argument("msg", type=str, required=True,
            help="The message must be provided", location="json")

        super(Logging, self).__init__()

    def get(self):
        all = ''
        for uuid in messages:
            all += f"{messages[uuid]}; "
        print("\tLOGGING-LOGS: Send messages")
        return {"msgs": all[:-2]}

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        msg = {
            "uuid": args["uuid"],
            "msg": args["msg"]
        }

        messages[msg["uuid"]] = msg["msg"]
        print(f"\tLOGGING-LOGS: New message is {msg['msg']} \nUuid is: {msg['uuid']}")
        return {"msg": marshal(msg, msgFields)}, 201

api.add_resource(Logging, "/logging")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)