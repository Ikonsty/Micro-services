from flask import Flask
from flask_restful import Api
from facade_controller import FacadeController
import os

app = Flask(__name__)
api = Api(app)

api.add_resource(FacadeController, "/")

if __name__ == "__main__":
    app.run(host=os.environ.get("HOST"), port=os.environ.get("PORT"))
