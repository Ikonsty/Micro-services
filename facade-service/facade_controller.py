from flask_restful import Resource, reqparse, marshal
from facade_service import FacadeService
from fields import msgFields


class FacadeController(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("msg", type=str, location="json")

        self.facade_service = FacadeService()

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
