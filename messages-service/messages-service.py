from flask import Flask, jsonify
import pika
from json import loads
import threading
import os
import time


app = Flask(__name__)
q_name = os.environ.get("Q_NAME")
rabbit_port = os.environ.get("RABBITMQ_PORT")
rabbit_host = os.environ.get("RABBITMQ_HOST")
no_connection = True
connection = None
# f_port = os.environ.get("FACADE_PORT")
# f_host = os.environ.get("FACADE_HOST")

# q_name = str(sys.argv[1])
while no_connection:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbit_host, rabbit_port)
        )
        no_connection = False
        print("\tMESSAGES-LOGS: RabbitMQ Connected")
    except:
        print("\tMESSAGES-LOGS: RabbitMQ no connection")
        time.sleep(5)


channel = connection.channel()
channel.queue_declare(queue=q_name)
msgs = []


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    msgs.append(loads(body))
    print(f"\tMESSAGES-LOGS: Recieved {body}")


def consume_messages():
    channel.basic_consume(queue=q_name, on_message_callback=callback, auto_ack=True)
    print("\tMESSAGES-LOGS: Waiting for messages")
    channel.start_consuming()


@app.route("/", methods=["GET"])
def index():
    print("\tMESSAGES-LOGS: GET request recieved. Send messages")
    parsed_msgs = " ".join([d["txt"] for d in msgs])
    print(parsed_msgs)
    return jsonify({"msgs": parsed_msgs})


if __name__ == "__main__":
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()

    app.run(host=os.environ.get("HOST"), port=os.environ.get("PORT"))
