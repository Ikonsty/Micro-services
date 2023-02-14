from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal, fields


msgFields = {
    "msgs": fields.String
}

app = Flask(__name__)
api = Api(app)

class Message(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("msgs", type=str, location="json")

        super(Message, self).__init__()

    def get(self):
        print("\tMESSAGES-LOGS: Not implemented yet")
        return {"msgs": "Not implemented yet"}

    def post(self):
        print("\tMESSAGES-LOGS: Not implemented yet")
        return {"msgs": "Not implemented yet"}

api.add_resource(Message, "/messages")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)