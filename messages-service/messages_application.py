from flask import Flask
import os
from messages_controller import MessageController
from messages_service import MessageService
import threading

app = Flask(__name__)

if __name__ == "__main__":
    q_name = os.environ.get("Q_NAME")
    rabbit_port = os.environ.get("RABBITMQ_PORT")
    rabbit_host = os.environ.get("RABBITMQ_HOST")
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")

    message_service = MessageService(q_name, rabbit_host, rabbit_port)
    message_controller = MessageController(message_service, app)

    consumer_thread = threading.Thread(target=message_service.consume_messages)
    consumer_thread.start()

    message_controller.register_routes()

    app.run(host=host, port=port)
