from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, engine
from data_writer import DataWriter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import vulnerability
import pika
import json

vulnerability.Base.metadata.create_all(bind=engine)
app = FastAPI()

RABBITMQ_HOST = "rabbitmq"

data_writer = DataWriter()


def send_message(queue: str, message: dict):
    """Send a message to a RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
    connection.close()

def receive_message(queue: str, db: Session):
    """Receive a message from a RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        if queue == "fetch_and_store":
            vulnerabilities = data_writer.fetch_data()
            if vulnerabilities:
                data_writer.write_to_db(vulnerabilities, db)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

#Get data from the api and store it in the db using data_writer
@app.post("/fetch-and-store")
async def fetch_and_store(db: Session = Depends(get_db)):
    send_message("fetch_and_store", {})
    receive_message("fetch_and_store", db)
    return {"status": "Data fetching and storing initiated."}


