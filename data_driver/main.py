import pika
from app.database import SessionLocal, init_db
from app.tasks import process_vulnerability

def start_rabbitmq_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='vulnerability_tasks')

    def callback(ch, method, properties, body):
        process_vulnerability(body)

    channel.basic_consume(queue='vulnerability_tasks', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()

if __name__ == "__main__":
    init_db()
    start_rabbitmq_listener()
