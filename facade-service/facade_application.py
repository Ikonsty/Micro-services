from flask import Flask
from flask_restful import Api
from facade_controller import FacadeController

app = Flask(__name__)
api = Api(app)

api.add_resource(FacadeController, "/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)