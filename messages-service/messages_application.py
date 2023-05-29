from flask import Flask
import os
from messages_controller import MessageController
import threading

app = Flask(__name__)

if __name__ == "__main__":
    port = os.environ.get("PORT")

    message_controller = MessageController(app)

    consumer_thread = threading.Thread(
        target=message_controller.get_service().consume_messages
    )
    consumer_thread.start()

    message_controller.register_routes()

    app.run(host="0.0.0.0", port=port)
