from flask_restful import fields
from json import JSONEncoder
import uuid

msgFields = {
    "msgs": fields.String
}

class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return JSONEncoder.default(self, obj)