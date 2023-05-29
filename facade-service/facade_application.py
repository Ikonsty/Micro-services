from flask import Flask
from facade_controller import FacadeController
import os

app = Flask(__name__)


if __name__ == "__main__":
    facadeController = FacadeController(app)

    facadeController.register_routes()

    app.run(host="0.0.0.0", port=os.environ.get("PORT"))
